// 人工标注核验平台前端逻辑

class AnnotationPlatform {
    constructor() {
        this.currentSample = null;
        this.datasetInfo = null;
        this.originalAnswers = {};
        this.userAnswers = {};
        this.loadingModal = null;
        this.roleColorCache = {};
        this.sampleRoleColorMap = {};
        this.relabelMode = false;  // 重标注模式标志
        this.totalRelabeled = 0;   // 已重标注数量
        this.visibleTasks = [];    // 重标注模式下可见的任务列表
        
        this.initializeEventListeners();
        this.loadAvailableFiles();
        this.checkRelabelStatus();
    }
    
    // 规范化角色名（用于颜色映射 key）
    normalizeRoleName(roleName) {
        return (roleName ?? '').toString().trim().toLowerCase();
    }

    // 为当前样本建立“角色->颜色”映射，确保同一场对话内不撞色
    buildSampleRoleColorMap() {
        this.sampleRoleColorMap = {};

        if (!this.currentSample) return;

        const names = [];
        const seen = new Set();

        const addName = (name) => {
            const key = this.normalizeRoleName(name);
            if (!key) return;
            if (seen.has(key)) return;
            seen.add(key);
            names.push({ key, displayName: name });
        };

        const scenario = this.currentSample.scenario_setup;
        if (scenario && Array.isArray(scenario.personas)) {
            scenario.personas.forEach(p => addName(p?.name));
        }

        const transcript = this.currentSample.dialogue_transcript;
        if (Array.isArray(transcript)) {
            transcript.forEach(t => addName(t?.speaker));
        }

        // 预定义色板（高对比度、易区分）
        const colors = [
            '#DC2626', // 红色
            '#2563EB', // 蓝色
            '#059669', // 绿色
            '#9333EA', // 紫色
            '#EA580C', // 橙色
            '#0891B2', // 青色
            '#CA8A04', // 金色
            '#BE185D', // 粉红
            '#4338CA', // 靠蓝
            '#15803D', // 深绿
        ];

        names.forEach((n, idx) => {
            this.sampleRoleColorMap[n.key] = colors[idx % colors.length];
        });
    }

    // 角色名颜色系统（优先使用本样本映射，保证同一场对话内不撞色）
    getRoleColor(roleName) {
        const key = this.normalizeRoleName(roleName);
        if (this.sampleRoleColorMap && this.sampleRoleColorMap[key]) {
            return this.sampleRoleColorMap[key];
        }
        if (this.roleColorCache[key]) {
            return this.roleColorCache[key];
        }
        
        // 简单的字符串哈希函数
        let hash = 0;
        for (let i = 0; i < key.length; i++) {
            hash = key.charCodeAt(i) + ((hash << 5) - hash);
        }
        
        // 预定义的色板（高对比度、易区分）
        const colors = [
            '#DC2626', // 红色
            '#2563EB', // 蓝色
            '#059669', // 绿色
            '#9333EA', // 紫色
            '#EA580C', // 橙色
            '#0891B2', // 青色
            '#CA8A04', // 金色
            '#BE185D', // 粉红
            '#4338CA', // 靠蓝
            '#15803D', // 深绿
        ];
        
        const colorIndex = Math.abs(hash) % colors.length;
        const color = colors[colorIndex];
        
        this.roleColorCache[key] = color;
        return color;
    }
    
    
    initializeEventListeners() {
        // 文件加载
        document.getElementById('loadBtn').addEventListener('click', () => {
            this.loadSelectedFile();
        });
        
        // 重标注模式按钮
        document.getElementById('relabelModeBtn').addEventListener('click', () => {
            this.toggleRelabelMode();
        });
        
        // 导航按钮
        document.getElementById('prevBtn').addEventListener('click', () => {
            this.navigate('prev');
        });
        
        document.getElementById('nextBtn').addEventListener('click', () => {
            this.navigate('next');
        });
        
        document.getElementById('gotoBtn').addEventListener('click', () => {
            const index = parseInt(document.getElementById('gotoInput').value) - 1;
            this.navigate('goto', index);
        });
        
        // 保存按钮
        document.getElementById('saveBtn').addEventListener('click', () => {
            this.saveAnnotation();
        });
        
        // 保存并下一个按钮
        document.getElementById('saveNextBtn').addEventListener('click', () => {
            this.saveAndNext();
        });
        
        // 选项选择事件委托
        document.addEventListener('change', (e) => {
            if (e.target.type === 'radio') {
                this.handleOptionChange(e.target);
            }
        });
    }
    
    async checkRelabelStatus() {
        try {
            const response = await fetch('/api/relabel/status');
            const data = await response.json();
            
            // 更新重标注按钮状态
            const relabelBtn = document.getElementById('relabelModeBtn');
            if (data.relabel_file_exists) {
                relabelBtn.classList.remove('disabled');
                relabelBtn.title = '点击进入重标注模式';
            } else {
                relabelBtn.classList.add('disabled');
                relabelBtn.title = '重标注数据文件不存在';
            }
        } catch (error) {
            console.error('检查重标注状态失败:', error);
        }
    }
    
    async toggleRelabelMode() {
        if (this.relabelMode) {
            // 退出重标注模式
            await this.exitRelabelMode();
        } else {
            // 进入重标注模式
            await this.enterRelabelMode();
        }
    }
    
    async enterRelabelMode() {
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/relabel/load');
            const data = await response.json();
            
            if (data.success) {
                this.relabelMode = true;
                this.datasetInfo = data.dataset_info;
                this.currentSample = data.sample;
                this.totalRelabeled = data.total_relabeled || 0;
                
                this.updateRelabelModeUI(true);
                
                // 恢复上次标注位置
                const lastIndex = this.getLastRelabelIndex();
                if (lastIndex > 0 && lastIndex < this.datasetInfo.total_samples) {
                    await this.navigate('goto', lastIndex);
                    this.showAlert(`已进入重标注模式，从第 ${lastIndex + 1} 个样本继续`, 'success');
                } else {
                    this.displaySample();
                    this.showAlert('已进入重标注模式', 'success');
                }
                
                this.showMainContent(true);
            } else {
                this.showAlert(data.error || '加载重标注数据失败', 'danger');
            }
        } catch (error) {
            console.error('进入重标注模式失败:', error);
            this.showAlert('进入重标注模式失败', 'danger');
        } finally {
            this.showLoading(false);
        }
    }
    
    // 获取上次重标注的位置
    getLastRelabelIndex() {
        try {
            const saved = localStorage.getItem('relabel_last_index');
            return saved ? parseInt(saved) : 0;
        } catch (e) {
            return 0;
        }
    }
    
    // 保存当前重标注位置
    saveRelabelIndex() {
        if (this.relabelMode && this.datasetInfo) {
            try {
                localStorage.setItem('relabel_last_index', this.datasetInfo.current_index.toString());
            } catch (e) {
                console.error('保存标注位置失败:', e);
            }
        }
    }
    
    // 保存并跳转到下一个样本
    async saveAndNext() {
        // 先保存当前标注
        await this.saveAnnotation();
        
        // 然后跳转到下一个样本
        if (this.datasetInfo && this.datasetInfo.current_index < this.datasetInfo.total_samples - 1) {
            await this.navigate('next');
            // 保存新位置
            this.saveRelabelIndex();
        } else {
            this.showAlert('已是最后一个样本', 'info');
        }
    }
    
    async exitRelabelMode() {
        try {
            await fetch('/api/relabel/exit');
            
            this.relabelMode = false;
            this.currentSample = null;
            this.datasetInfo = null;
            this.totalRelabeled = 0;
            
            this.updateRelabelModeUI(false);
            this.showMainContent(false);
            this.showAlert('已退出重标注模式', 'info');
        } catch (error) {
            console.error('退出重标注模式失败:', error);
        }
    }
    
    updateRelabelModeUI(isRelabelMode) {
        const relabelBtn = document.getElementById('relabelModeBtn');
        const relabelModeTag = document.getElementById('relabelModeTag');
        const relabeledCountTag = document.getElementById('relabeledCountTag');
        const fileSelect = document.getElementById('fileSelect');
        const loadBtn = document.getElementById('loadBtn');
        
        if (isRelabelMode) {
            relabelBtn.classList.add('active');
            relabelBtn.innerHTML = '<i class="fas fa-times"></i><span class="btn-text">退出重标注</span>';
            relabelModeTag.style.display = 'inline-flex';
            relabeledCountTag.style.display = 'inline-flex';
            document.getElementById('headerRelabeledCount').textContent = this.totalRelabeled;
            fileSelect.disabled = true;
            loadBtn.disabled = true;
        } else {
            relabelBtn.classList.remove('active');
            relabelBtn.innerHTML = '<i class="fas fa-redo-alt"></i><span class="btn-text">重标注模式</span>';
            relabelModeTag.style.display = 'none';
            relabeledCountTag.style.display = 'none';
            fileSelect.disabled = false;
            loadBtn.disabled = false;
        }
    }
    
    async loadAvailableFiles() {
        try {
            const response = await fetch('/api/files');
            const data = await response.json();
            
            const select = document.getElementById('fileSelect');
            select.innerHTML = '<option value="">选择数据文件...</option>';
            
            data.files.forEach(file => {
                const option = document.createElement('option');
                option.value = file;
                option.textContent = file;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('加载文件列表失败:', error);
            this.showAlert('加载文件列表失败', 'danger');
        }
    }
    
    async loadSelectedFile() {
        const filename = document.getElementById('fileSelect').value;
        if (!filename) {
            this.showAlert('请选择一个文件', 'warning');
            return;
        }
        
        this.showLoading(true);
        
        try {
            console.log('开始请求文件:', filename);
            const response = await fetch(`/api/load/${filename}`);
            console.log('收到响应:', response.status);
            
            const data = await response.json();
            console.log('解析数据:', data);
            
            if (data.success) {
                console.log('数据加载成功，开始显示');
                this.datasetInfo = data.dataset_info;
                this.currentSample = data.sample;
                console.log('当前样本:', this.currentSample);
                
                this.displaySample();
                this.showMainContent(true);
                this.showAlert('文件加载成功', 'success');
            } else {
                console.error('服务器返回错误:', data.error);
                this.showAlert(data.error || '文件加载失败', 'danger');
            }
        } catch (error) {
            console.error('加载文件失败:', error);
            this.showAlert('加载文件失败', 'danger');
        } finally {
            console.log('关闭加载提示');
            this.showLoading(false);
        }
    }
    
    async navigate(action, index = null) {
        const payload = { action };
        if (index !== null) {
            payload.index = index;
        }
        
        try {
            const response = await fetch('/api/navigate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.datasetInfo = data.dataset_info;
                this.currentSample = data.sample;
                this.displaySample();
            } else {
                this.showAlert(data.error || '导航失败', 'warning');
            }
        } catch (error) {
            console.error('导航失败:', error);
            this.showAlert('导航失败', 'danger');
        }
    }
    
    displaySample() {
        console.log('开始显示样本');
        if (!this.currentSample) {
            console.error('没有当前样本数据');
            return;
        }

        // 为当前样本建立角色颜色映射（同一场对话内不同角色不重复）
        this.buildSampleRoleColorMap();
        
        console.log('显示数据集信息');
        this.displayDatasetInfo();
        
        console.log('显示情境设定');
        this.displayScenario();
        
        console.log('显示对话内容');
        this.displayDialogue();
        
        console.log('显示评测标签');
        this.displayLabels();
        
        console.log('更新导航状态');
        this.updateNavigation();
        
        console.log('样本显示完成');
    }
    
    displayDatasetInfo() {
        if (!this.datasetInfo) return;
        
        // 更新顶部数据集标签
        document.getElementById('headerTotalSamples').textContent = this.datasetInfo.total_samples || 0;
        document.getElementById('headerProgress').textContent = 
            `${this.datasetInfo.current_index + 1}/${this.datasetInfo.total_samples}`;
        document.getElementById('headerModel').textContent = this.datasetInfo.model || '未知';
        
        // 显示数据集标签
        document.getElementById('datasetTags').style.display = 'flex';
    }
    
    displayScenario() {
        const scenario = this.currentSample.scenario_setup;
        
        // 更新情境面板 Badge
        document.getElementById('benchmarkIdBadge').textContent = this.currentSample.benchmark_id;
        document.getElementById('metaThemeBadge').textContent = this.currentSample.meta_theme || '自由主题';
        
        // 更新场景描述
        document.getElementById('scenarioDescription').textContent = scenario.scenario_description;
        
        // 显示角色情报（单一容器列表布局）
        const personasContainer = document.getElementById('personas');
        personasContainer.innerHTML = '';
        
        scenario.personas.forEach(persona => {
            // 获取角色颜色（与对话中一致）
            const roleColor = this.getRoleColor(persona.name);
            const initial = persona.name.charAt(0).toUpperCase();
            
            const personaItem = document.createElement('div');
            personaItem.className = 'persona-item';
            personaItem.innerHTML = `
                <div class="persona-item-bar" style="background-color: ${roleColor};"></div>
                <div class="persona-item-content">
                    <div class="persona-item-header">
                        <div class="persona-item-initial" style="background-color: ${roleColor};">${initial}</div>
                        <span class="persona-item-name">${persona.name}</span>
                    </div>
                    <div class="persona-public">
                        <span class="persona-icon">👁️</span>
                        <span>${persona.public_goal}</span>
                    </div>
                    <div class="persona-hidden">
                        <span class="persona-icon">🔒</span>
                        <span>${persona.private_motive}</span>
                    </div>
                </div>
            `;
            personasContainer.appendChild(personaItem);
        });
    }
    
    displayDialogue() {
        const dialogueTranscript = this.currentSample.dialogue_transcript;
        const evaluationTrigger = this.currentSample.evaluation_trigger;
        const dialogueContainer = document.getElementById('dialogueContent');
        
        // 更新对话统计信息
        document.getElementById('dialogueTurns').textContent = dialogueTranscript.length;
        document.getElementById('criticalMoment').textContent = evaluationTrigger.trigger_turn_id;
        
        // 创建时间线容器
        dialogueContainer.innerHTML = '';
        const timelineContainer = document.createElement('div');
        timelineContainer.className = 'timeline-container';
        
        // 叙事时间线渲染
        dialogueTranscript.forEach((turn) => {
            const turnDiv = document.createElement('div');
            const isCritical = turn.turn === evaluationTrigger.trigger_turn_id;
            
            turnDiv.className = `dialogue-turn ${isCritical ? 'critical' : ''}`;
            
            // 获取角色颜色
            const roleColor = this.getRoleColor(turn.speaker);
            const initial = turn.speaker.charAt(0).toUpperCase();
            
            // 构建时间线节点 HTML
            let html = `
                <span class="turn-number">Turn ${turn.turn}</span>
                <div class="turn-avatar" style="background-color: ${roleColor};">${initial}</div>
                <div class="turn-card">
                    <div class="turn-card-bar" style="background-color: ${roleColor};"></div>
                    <div class="turn-card-content">
                        <div class="turn-header">
                            <span class="speaker-name" style="color: ${roleColor};">${turn.speaker}</span>
                            <span class="turn-id">#${turn.turn}</span>
            `;
            
            if (isCritical) {
                html += `<span class="critical-badge">关键时刻</span>`;
            }
            
            html += `
                        </div>
                        <p class="turn-content">${turn.line}</p>
                    </div>
                </div>
            `;
            
            turnDiv.innerHTML = html;
            timelineContainer.appendChild(turnDiv);
        });
        
        dialogueContainer.appendChild(timelineContainer);
    }
    
    displayLabels() {
        const labels = this.currentSample.evaluation_labels;
        
        // 重标注模式下，只显示冲突的任务
        if (this.relabelMode) {
            this.displayRelabelLabels(labels);
            return;
        }
        
        this.originalAnswers = {
            atmosphere: labels.atmosphere_recognition.correct_answer_index + 1,
            ky: labels.ky_test.correct_answer_index + 1,
            intent: labels.subtext_deciphering.correct_answer_index + 1
        };
        
        // 显示所有标签页
        this.showAllTabs();
        
        // 氛围识别
        this.displayQuestion('atmosphere', {
            question: labels.atmosphere_recognition.question,
            options: labels.atmosphere_recognition.mcq_options,
            correct_answer: this.originalAnswers.atmosphere
        });
        
        // KY测试
        this.displayQuestion('ky', {
            question: labels.ky_test.question,
            options: labels.ky_test.mcq_options,
            correct_answer: this.originalAnswers.ky
        });
        
        // 意图推断
        this.displayQuestion('intent', {
            question: labels.subtext_deciphering.question,
            options: labels.subtext_deciphering.mcq_options,
            correct_answer: this.originalAnswers.intent
        });
        
        // 重置用户答案和状态
        this.userAnswers = {};
        this.updateComparison();
        this.resetTaskStatus();
        
        // 重置到第一个标签页
        const firstTab = new bootstrap.Tab(document.getElementById('atmosphere-tab'));
        firstTab.show();
    }
    
    showAllTabs() {
        // 显示所有标签页
        document.getElementById('atmosphere-tab').parentElement.style.display = '';
        document.getElementById('ky-tab').parentElement.style.display = '';
        document.getElementById('intent-tab').parentElement.style.display = '';
    }
    
    displayRelabelLabels(labels) {
        // 获取冲突的任务类型
        const conflictTaskTypes = this.currentSample.conflict_task_types || [];
        
        // 任务类型映射
        const taskTypeMap = {
            'atmosphere_recognition': { tab: 'atmosphere', name: '氛围识别' },
            'ky_test': { tab: 'ky', name: 'KY测试' },
            'subtext_deciphering': { tab: 'intent', name: '意图推断' }
        };
        
        // 隐藏所有标签页
        document.getElementById('atmosphere-tab').parentElement.style.display = 'none';
        document.getElementById('ky-tab').parentElement.style.display = 'none';
        document.getElementById('intent-tab').parentElement.style.display = 'none';
        
        this.originalAnswers = {};
        this.visibleTasks = [];  // 重置可见任务列表
        let firstVisibleTab = null;
        
        // 只显示冲突的任务
        conflictTaskTypes.forEach(taskType => {
            const mapping = taskTypeMap[taskType];
            if (!mapping || !labels[taskType]) return;
            
            const tabElement = document.getElementById(`${mapping.tab}-tab`);
            tabElement.parentElement.style.display = '';
            
            // 记录可见任务
            this.visibleTasks.push(mapping.tab);
            
            if (!firstVisibleTab) {
                firstVisibleTab = tabElement;
            }
            
            const labelData = labels[taskType];
            const answerKey = mapping.tab === 'intent' ? 'intent' : mapping.tab;
            this.originalAnswers[answerKey] = labelData.correct_answer_index + 1;
            
            // 显示问题，并添加冲突信息
            this.displayRelabelQuestion(mapping.tab, {
                question: labelData.question,
                options: labelData.mcq_options,
                correct_answer: labelData.correct_answer_index + 1,
                conflict_info: labelData.conflict_info
            });
        });
        
        // 重置用户答案和状态
        this.userAnswers = {};
        this.updateComparison();
        this.resetTaskStatus();
        
        // 显示第一个可见的标签页
        if (firstVisibleTab) {
            const tab = new bootstrap.Tab(firstVisibleTab);
            tab.show();
        }
    }
    
    displayRelabelQuestion(type, questionData) {
        const questionElement = document.getElementById(`${type}Question`);
        const optionsContainer = document.getElementById(`${type}Options`);
        
        // 显示问题
        questionElement.textContent = questionData.question;
        optionsContainer.innerHTML = '';
        
        // 显示冲突信息
        if (questionData.conflict_info) {
            const conflictDiv = document.createElement('div');
            conflictDiv.className = 'conflict-info-box';
            
            let conflictHtml = `<div class="conflict-header">
                <i class="fas fa-exclamation-triangle"></i>
                <span>投票冲突信息</span>
            </div>`;
            
            conflictHtml += `<div class="conflict-reason">${questionData.conflict_info.reason || '模型投票未达成一致'}</div>`;
            
            // 显示各模型投票
            if (questionData.conflict_info.model_votes) {
                conflictHtml += '<div class="model-votes"><strong>各模型投票:</strong><ul>';
                for (const [model, vote] of Object.entries(questionData.conflict_info.model_votes)) {
                    const optionLetter = String.fromCharCode(65 + vote);  // 0->A, 1->B, etc.
                    conflictHtml += `<li><span class="model-name">${model}</span>: <span class="vote-option">选项${optionLetter}</span></li>`;
                }
                conflictHtml += '</ul></div>';
            }
            
            // 显示投票统计
            if (questionData.conflict_info.vote_details) {
                conflictHtml += '<div class="vote-stats"><strong>投票统计:</strong> ';
                const stats = [];
                for (const [option, count] of Object.entries(questionData.conflict_info.vote_details)) {
                    const optionLetter = String.fromCharCode(65 + parseInt(option));
                    stats.push(`选项${optionLetter}: ${count}票`);
                }
                conflictHtml += stats.join(', ') + '</div>';
            }
            
            conflictDiv.innerHTML = conflictHtml;
            optionsContainer.appendChild(conflictDiv);
        }
        
        // 显示选项
        questionData.options.forEach((option, index) => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option-item';
            
            const optionId = `${type}_option_${index}`;
            const isOriginalAnswer = (index + 1) === questionData.correct_answer;
            
            optionDiv.innerHTML = `
                <input type="radio" id="${optionId}" name="${type}" value="${index + 1}" class="option-radio">
                <label for="${optionId}" class="option-label ${isOriginalAnswer ? 'original' : ''}">
                    <span class="option-text">${option}</span>
                </label>
            `;
            
            optionsContainer.appendChild(optionDiv);
        });
        
        // 添加差异警告提示容器
        const warningDiv = document.createElement('div');
        warningDiv.id = `${type}_warning`;
        warningDiv.className = 'difference-warning';
        warningDiv.innerHTML = `
            <span class="difference-warning-icon">⚠️</span>
            <span>您的选择与原始标签不一致</span>
        `;
        optionsContainer.appendChild(warningDiv);
    }
    
    resetTaskStatus() {
        // 清除任务状态
        ['atmosphere', 'ky', 'intent'].forEach(type => {
            const statusElement = document.getElementById(`${type}Status`);
            if (statusElement) {
                statusElement.classList.remove('completed');
            }
        });
        
        // 隐藏下一题按钮和完成提示
        ['atmosphereNext', 'kyNext'].forEach(btnId => {
            const btn = document.getElementById(btnId);
            if (btn) btn.style.display = 'none';
        });
        
        const completeHint = document.getElementById('intentComplete');
        if (completeHint) completeHint.style.display = 'none';
    }
    
    displayQuestion(type, questionData) {
        const questionElement = document.getElementById(`${type}Question`);
        const optionsContainer = document.getElementById(`${type}Options`);
        
        questionElement.textContent = questionData.question;
        optionsContainer.innerHTML = '';
        
        questionData.options.forEach((option, index) => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option-item';
            
            const optionId = `${type}_option_${index}`;
            const isOriginalAnswer = (index + 1) === questionData.correct_answer;
            
            optionDiv.innerHTML = `
                <input type="radio" id="${optionId}" name="${type}" value="${index + 1}" class="option-radio">
                <label for="${optionId}" class="option-label ${isOriginalAnswer ? 'original' : ''}">
                    <span class="option-text">${option}</span>
                </label>
            `;
            
            optionsContainer.appendChild(optionDiv);
        });
        
        // 添加差异警告提示容器
        const warningDiv = document.createElement('div');
        warningDiv.id = `${type}_warning`;
        warningDiv.className = 'difference-warning';
        warningDiv.innerHTML = `
            <span class="difference-warning-icon">⚠️</span>
            <span>您的选择与 AI 原始判断不一致</span>
        `;
        optionsContainer.appendChild(warningDiv);
    }
    
    handleOptionChange(radio) {
        const questionType = radio.name;
        const selectedValue = parseInt(radio.value);
        
        // 更新用户答案
        this.userAnswers[questionType] = selectedValue;
        
        // 更新选项样式
        this.updateOptionStyles(questionType, selectedValue);
        
        // 更新对比信息
        this.updateComparison();
        
        // 更新任务状态
        this.updateTaskStatus(questionType);
        
        // 显示下一题按钮或完成提示
        this.showNextTaskButton(questionType);
    }
    
    updateOptionStyles(questionType, selectedValue) {
        const container = document.getElementById(`${questionType}Options`);
        const labels = container.querySelectorAll('.option-label');
        const warningElement = document.getElementById(`${questionType}_warning`);
        
        // 检查是否与原始答案不同
        const isDifferent = selectedValue !== this.originalAnswers[questionType];
        
        labels.forEach((label, index) => {
            label.classList.remove('selected');
            
            if (index + 1 === selectedValue) {
                label.classList.add('selected');
            }
        });
        
        // 显示或隐藏差异警告
        if (warningElement) {
            if (isDifferent) {
                warningElement.classList.add('show');
            } else {
                warningElement.classList.remove('show');
            }
        }
    }
    
    updateComparison() {
        const comparisonInfo = document.getElementById('comparisonInfo');
        const comparisonDetails = document.getElementById('comparisonDetails');
        
        let hasComparison = false;
        let comparisonHtml = '';
        
        const questionTypes = {
            'atmosphere': '氛围识别',
            'ky': 'KY测试',
            'intent': '意图推断'
        };
        
        Object.keys(questionTypes).forEach(type => {
            if (this.userAnswers[type] !== undefined) {
                hasComparison = true;
                const original = this.originalAnswers[type];
                const user = this.userAnswers[type];
                const isSame = original === user;
                
                comparisonHtml += `
                    <div class="comparison-item ${isSame ? 'comparison-same' : 'comparison-different'}">
                        <strong>${questionTypes[type]}:</strong> 
                        AI答案: 选项${original} | 您的答案: 选项${user}
                    </div>
                `;
            }
        });
        
        if (hasComparison) {
            comparisonDetails.innerHTML = comparisonHtml;
            comparisonInfo.style.display = 'block';
        } else {
            comparisonInfo.style.display = 'none';
        }
    }
    
    updateTaskStatus(questionType) {
        const statusElement = document.getElementById(`${questionType}Status`);
        if (statusElement && this.userAnswers[questionType]) {
            statusElement.classList.add('completed');
        }
    }
    
    showNextTaskButton(questionType) {
        // 重标注模式下使用动态任务列表
        if (this.relabelMode && this.visibleTasks.length > 0) {
            this.showRelabelNextTaskButton(questionType);
            return;
        }
        
        const taskMap = {
            'atmosphere': { next: 'ky', btnId: 'atmosphereNext', tabId: 'ky-tab' },
            'ky': { next: 'intent', btnId: 'kyNext', tabId: 'intent-tab' },
            'intent': { next: null, btnId: null, completeId: 'intentComplete' }
        };
        
        const task = taskMap[questionType];
        if (!task) return;
        
        if (task.next) {
            // 显示下一题按钮
            const nextBtn = document.getElementById(task.btnId);
            if (nextBtn) {
                nextBtn.style.display = 'flex';
                nextBtn.onclick = () => {
                    const nextTab = new bootstrap.Tab(document.getElementById(task.tabId));
                    nextTab.show();
                    nextBtn.style.display = 'none';
                };
            }
        } else {
            // 显示完成提示
            const completeHint = document.getElementById(task.completeId);
            if (completeHint) {
                completeHint.style.display = 'flex';
            }
        }
    }
    
    showRelabelNextTaskButton(questionType) {
        // 找到当前任务在可见任务列表中的位置
        const currentIndex = this.visibleTasks.indexOf(questionType);
        if (currentIndex === -1) return;
        
        const btnIdMap = {
            'atmosphere': 'atmosphereNext',
            'ky': 'kyNext',
            'intent': null
        };
        
        const btnId = btnIdMap[questionType];
        const isLastTask = currentIndex === this.visibleTasks.length - 1;
        
        if (isLastTask) {
            // 最后一个任务，显示完成提示
            const completeHint = document.getElementById('intentComplete');
            if (completeHint) {
                completeHint.style.display = 'flex';
            }
        } else if (btnId) {
            // 显示下一题按钮
            const nextBtn = document.getElementById(btnId);
            if (nextBtn) {
                nextBtn.style.display = 'flex';
                const nextTask = this.visibleTasks[currentIndex + 1];
                nextBtn.onclick = async () => {
                    // 先保存当前标注
                    await this.saveCurrentAnnotation();
                    // 然后跳转到下一题
                    const nextTab = new bootstrap.Tab(document.getElementById(`${nextTask}-tab`));
                    nextTab.show();
                    nextBtn.style.display = 'none';
                };
            }
        }
    }
    
    async saveCurrentAnnotation() {
        // 保存当前标注（不检查是否所有任务都已完成）
        if (Object.keys(this.userAnswers).length === 0) {
            return; // 没有选择任何答案，不保存
        }
        
        let annotations;
        
        if (this.relabelMode) {
            annotations = {};
            const conflictTaskTypes = this.currentSample.conflict_task_types || [];
            
            const taskTypeMap = {
                'atmosphere_recognition': 'atmosphere',
                'ky_test': 'ky',
                'subtext_deciphering': 'intent'
            };
            
            conflictTaskTypes.forEach(taskType => {
                const answerKey = taskTypeMap[taskType];
                if (this.currentSample.evaluation_labels[taskType] && this.userAnswers[answerKey]) {
                    annotations[taskType] = {
                        ...this.currentSample.evaluation_labels[taskType],
                        correct_answer_index: this.userAnswers[answerKey] - 1
                    };
                    delete annotations[taskType].conflict_info;
                }
            });
        } else {
            return; // 普通模式不使用此方法
        }
        
        if (Object.keys(annotations).length === 0) {
            return;
        }
        
        try {
            const response = await fetch('/api/annotate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sample_id: this.currentSample.benchmark_id,
                    annotations: annotations
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // 更新已标注计数（只在第一次保存时增加）
                // 注意：这里不增加计数，因为可能是同一样本的多次保存
            }
        } catch (error) {
            console.error('保存失败:', error);
        }
    }
    
    async saveAnnotation() {
        if (Object.keys(this.userAnswers).length === 0) {
            this.showAlert('请至少选择一个答案', 'warning');
            return;
        }
        
        let annotations;
        
        if (this.relabelMode) {
            // 重标注模式：只保存冲突任务的标注
            annotations = {};
            const conflictTaskTypes = this.currentSample.conflict_task_types || [];
            
            const taskTypeMap = {
                'atmosphere_recognition': 'atmosphere',
                'ky_test': 'ky',
                'subtext_deciphering': 'intent'
            };
            
            conflictTaskTypes.forEach(taskType => {
                const answerKey = taskTypeMap[taskType];
                if (this.currentSample.evaluation_labels[taskType]) {
                    annotations[taskType] = {
                        ...this.currentSample.evaluation_labels[taskType],
                        correct_answer_index: (this.userAnswers[answerKey] || this.originalAnswers[answerKey]) - 1
                    };
                    // 移除conflict_info，不需要保存到结果中
                    delete annotations[taskType].conflict_info;
                }
            });
        } else {
            // 普通模式
            annotations = {
                atmosphere_recognition: {
                    ...this.currentSample.evaluation_labels.atmosphere_recognition,
                    correct_answer_index: (this.userAnswers.atmosphere || this.originalAnswers.atmosphere) - 1
                },
                ky_test: {
                    ...this.currentSample.evaluation_labels.ky_test,
                    correct_answer_index: (this.userAnswers.ky || this.originalAnswers.ky) - 1
                },
                subtext_deciphering: {
                    ...this.currentSample.evaluation_labels.subtext_deciphering,
                    correct_answer_index: (this.userAnswers.intent || this.originalAnswers.intent) - 1
                }
            };
        }
        
        try {
            const response = await fetch('/api/annotate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sample_id: this.currentSample.benchmark_id,
                    annotations: annotations
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showAlert('标注已保存', 'success');
                
                // 重标注模式下更新已标注计数
                if (this.relabelMode) {
                    this.totalRelabeled++;
                    document.getElementById('headerRelabeledCount').textContent = this.totalRelabeled;
                }
            } else {
                this.showAlert(data.error || '保存失败', 'danger');
            }
        } catch (error) {
            console.error('保存失败:', error);
            this.showAlert('保存失败', 'danger');
        }
    }
    
    updateNavigation() {
        if (!this.datasetInfo) return;
        
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const gotoInput = document.getElementById('gotoInput');
        
        prevBtn.disabled = this.datasetInfo.current_index === 0;
        nextBtn.disabled = this.datasetInfo.current_index >= this.datasetInfo.total_samples - 1;
        
        gotoInput.max = this.datasetInfo.total_samples;
        gotoInput.value = this.datasetInfo.current_index + 1;
    }
    
    showMainContent(show) {
        const elements = ['infoSidebar', 'dialogueCard', 'labelsCard'];
        elements.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.style.display = show ? 'flex' : 'none';
            }
        });
        
        // 显示/隐藏底部导航栏
        const bottomBar = document.getElementById('bottomBar');
        if (bottomBar) {
            bottomBar.style.display = show ? 'block' : 'none';
        }
    }
    
    showLoading(show) {
        if (!this.loadingModal) {
            this.loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        }
        
        if (show) {
            this.loadingModal.show();
        } else {
            this.loadingModal.hide();
        }
    }
    
    showAlert(message, type) {
        // 创建临时提示
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // 3秒后自动消失
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 3000);
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new AnnotationPlatform();
});
