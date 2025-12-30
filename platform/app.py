"""
人工标注核验平台 - Flask后端
"""
import os
import json
import copy
from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
from annotation_analysis import AnnotationAnalyzer

app = Flask(__name__)

# 配置
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "data_generator" / "data"
ANNOTATED_DIR = BASE_DIR / "annotated_data"
ANNOTATED_DIR.mkdir(exist_ok=True)

# 重标注模式配置
RELABEL_DIR = BASE_DIR.parent / "relabel"
RELABEL_DATA_FILE = RELABEL_DIR / "relabel_whole_data.json"
RELABELED_OUTPUT_FILE = RELABEL_DIR / "relabeled_data.json"

print(f"数据目录: {DATA_DIR.absolute()}")
print(f"数据目录存在: {DATA_DIR.exists()}")
if DATA_DIR.exists():
    print(f"数据文件: {list(DATA_DIR.glob('*.json'))}")

class AnnotationPlatform:
    """标注平台核心逻辑"""
    
    def __init__(self):
        self.current_file = None
        self.current_data = None
        self.current_sample_index = 0
        self.relabel_mode = False  # 重标注模式标志
        self.relabeled_data = None  # 重标注结果数据
        
    def load_dataset(self, filename):
        """加载数据集"""
        file_path = DATA_DIR / filename
        print(f"尝试加载文件: {file_path.absolute()}")
        print(f"文件存在: {file_path.exists()}")
        
        if not file_path.exists():
            print(f"文件不存在: {file_path}")
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.current_data = json.load(f)
            self.current_file = filename
            self.current_sample_index = 0
            print(f"成功加载文件，样本数: {len(self.current_data.get('samples', []))}")
            return True
        except Exception as e:
            print(f"加载文件失败: {e}")
            return False
    
    def get_available_files(self):
        """获取可用的数据文件"""
        if not DATA_DIR.exists():
            return []
        return [f.name for f in DATA_DIR.glob("*.json")]
    
    def get_current_sample(self):
        """获取当前样本"""
        if not self.current_data or not self.current_data.get('samples'):
            return None
            
        samples = self.current_data['samples']
        if self.current_sample_index >= len(samples):
            return None
            
        return samples[self.current_sample_index]
    
    def get_dataset_info(self):
        """获取数据集信息"""
        if not self.current_data:
            return None
            
        info = self.current_data.get('dataset_info', {})
        info['current_index'] = self.current_sample_index
        info['total_samples'] = len(self.current_data.get('samples', []))
        return info
    
    def save_annotation(self, sample_id, annotations):
        """保存标注结果"""
        if not self.current_data:
            return False
        
        if self.relabel_mode:
            # 重标注模式：保存到relabeled_data.json
            return self.save_relabel_annotation(sample_id, annotations)
            
        # 创建带标注的数据副本
        annotated_data = copy.deepcopy(self.current_data)
        
        # 更新对应样本的标注
        for sample in annotated_data['samples']:
            if sample['benchmark_id'] == sample_id:
                # 保存原始答案
                if 'original_labels' not in sample:
                    sample['original_labels'] = copy.deepcopy(sample['evaluation_labels'])
                
                # 更新为人工标注答案
                sample['evaluation_labels'] = annotations
                sample['human_annotated'] = True
                break
        
        # 保存到标注文件夹
        annotated_file = ANNOTATED_DIR / f"annotated_{self.current_file}"
        with open(annotated_file, 'w', encoding='utf-8') as f:
            json.dump(annotated_data, f, ensure_ascii=False, indent=2)
            
        return True
    
    def load_relabel_data(self):
        """加载重标注数据"""
        if not RELABEL_DATA_FILE.exists():
            print(f"重标注数据文件不存在: {RELABEL_DATA_FILE}")
            return False
        
        try:
            with open(RELABEL_DATA_FILE, 'r', encoding='utf-8') as f:
                self.current_data = json.load(f)
            self.current_file = "relabel_whole_data.json"
            self.current_sample_index = 0
            self.relabel_mode = True
            
            # 加载已有的重标注结果（如果存在）
            if RELABELED_OUTPUT_FILE.exists():
                with open(RELABELED_OUTPUT_FILE, 'r', encoding='utf-8') as f:
                    self.relabeled_data = json.load(f)
            else:
                # 初始化重标注结果数据结构
                self.relabeled_data = {
                    "dataset_info": {
                        "description": "人工重标注结果",
                        "source": str(RELABEL_DATA_FILE),
                        "total_relabeled": 0
                    },
                    "relabeled_samples": []
                }
            
            print(f"成功加载重标注数据，样本数: {len(self.current_data.get('samples', []))}")
            return True
        except Exception as e:
            print(f"加载重标注数据失败: {e}")
            return False
    
    def save_relabel_annotation(self, sample_id, annotations):
        """保存重标注结果到relabeled_data.json"""
        if not self.relabeled_data:
            return False
        
        # 查找当前样本
        current_sample = None
        for sample in self.current_data['samples']:
            if sample['benchmark_id'] == sample_id:
                current_sample = sample
                break
        
        if not current_sample:
            return False
        
        # 构建重标注记录
        relabel_record = {
            "benchmark_id": sample_id,
            "conflict_task_types": current_sample.get('conflict_task_types', []),
            "human_annotations": annotations,
            "human_annotated": True
        }
        
        # 更新或添加记录
        found = False
        for i, record in enumerate(self.relabeled_data['relabeled_samples']):
            if record['benchmark_id'] == sample_id:
                self.relabeled_data['relabeled_samples'][i] = relabel_record
                found = True
                break
        
        if not found:
            self.relabeled_data['relabeled_samples'].append(relabel_record)
        
        # 更新统计
        self.relabeled_data['dataset_info']['total_relabeled'] = len(self.relabeled_data['relabeled_samples'])
        
        # 保存到文件
        with open(RELABELED_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.relabeled_data, f, ensure_ascii=False, indent=2)
        
        return True
    
    def exit_relabel_mode(self):
        """退出重标注模式"""
        self.relabel_mode = False
        self.relabeled_data = None
        self.current_data = None
        self.current_file = None
        self.current_sample_index = 0
    
    def next_sample(self):
        """切换到下一个样本"""
        if not self.current_data:
            return False
            
        total_samples = len(self.current_data.get('samples', []))
        if self.current_sample_index < total_samples - 1:
            self.current_sample_index += 1
            return True
        return False
    
    def prev_sample(self):
        """切换到上一个样本"""
        if self.current_sample_index > 0:
            self.current_sample_index -= 1
            return True
        return False
    
    def goto_sample(self, index):
        """跳转到指定样本"""
        if not self.current_data:
            return False
            
        total_samples = len(self.current_data.get('samples', []))
        if 0 <= index < total_samples:
            self.current_sample_index = index
            return True
        return False

# 全局平台实例
platform = AnnotationPlatform()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/files')
def get_files():
    """获取可用文件列表"""
    files = platform.get_available_files()
    return jsonify({'files': files})

@app.route('/api/load/<filename>')
def load_file(filename):
    """加载指定文件"""
    success = platform.load_dataset(filename)
    if success:
        return jsonify({
            'success': True,
            'dataset_info': platform.get_dataset_info(),
            'sample': platform.get_current_sample()
        })
    else:
        return jsonify({'success': False, 'error': '文件加载失败'})

@app.route('/api/sample')
def get_sample():
    """获取当前样本"""
    sample = platform.get_current_sample()
    dataset_info = platform.get_dataset_info()
    
    if sample:
        return jsonify({
            'success': True,
            'sample': sample,
            'dataset_info': dataset_info
        })
    else:
        return jsonify({'success': False, 'error': '没有可用样本'})

@app.route('/api/navigate', methods=['POST'])
def navigate():
    """样本导航"""
    data = request.get_json()
    action = data.get('action')
    
    success = False
    if action == 'next':
        success = platform.next_sample()
    elif action == 'prev':
        success = platform.prev_sample()
    elif action == 'goto':
        index = data.get('index', 0)
        success = platform.goto_sample(index)
    
    if success:
        return jsonify({
            'success': True,
            'sample': platform.get_current_sample(),
            'dataset_info': platform.get_dataset_info()
        })
    else:
        return jsonify({'success': False, 'error': '导航失败'})

@app.route('/api/annotate', methods=['POST'])
def annotate():
    """保存标注"""
    data = request.get_json()
    sample_id = data.get('sample_id')
    annotations = data.get('annotations')
    
    success = platform.save_annotation(sample_id, annotations)
    
    if success:
        return jsonify({'success': True, 'message': '标注已保存'})
    else:
        return jsonify({'success': False, 'error': '保存失败'})

@app.route('/api/analysis')
def get_analysis():
    """获取标注分析结果"""
    if not platform.current_file:
        return jsonify({'success': False, 'error': '没有加载数据文件'})
    
    annotated_file = ANNOTATED_DIR / f"annotated_{platform.current_file}"
    
    if not annotated_file.exists():
        return jsonify({'success': False, 'error': '没有找到标注文件'})
    
    try:
        analyzer = AnnotationAnalyzer(str(annotated_file))
        metrics = analyzer.calculate_agreement_metrics()
        report = analyzer.generate_detailed_report()
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'report': report,
            'annotated_file': str(annotated_file)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'分析失败: {str(e)}'})

@app.route('/analysis')
def analysis_page():
    """分析页面"""
    return render_template('analysis.html')

# ==================== 重标注模式API ====================

@app.route('/api/relabel/load')
def load_relabel_data():
    """加载重标注数据"""
    success = platform.load_relabel_data()
    if success:
        return jsonify({
            'success': True,
            'dataset_info': platform.get_dataset_info(),
            'sample': platform.get_current_sample(),
            'relabel_mode': True,
            'total_relabeled': len(platform.relabeled_data.get('relabeled_samples', [])) if platform.relabeled_data else 0
        })
    else:
        return jsonify({'success': False, 'error': '重标注数据加载失败'})

@app.route('/api/relabel/exit')
def exit_relabel_mode():
    """退出重标注模式"""
    platform.exit_relabel_mode()
    return jsonify({'success': True, 'message': '已退出重标注模式'})

@app.route('/api/relabel/status')
def get_relabel_status():
    """获取重标注模式状态"""
    return jsonify({
        'relabel_mode': platform.relabel_mode,
        'relabel_file_exists': RELABEL_DATA_FILE.exists(),
        'total_relabeled': len(platform.relabeled_data.get('relabeled_samples', [])) if platform.relabeled_data else 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
