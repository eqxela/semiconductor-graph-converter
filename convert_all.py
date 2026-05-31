#!/usr/bin/env python3
import os
import sys
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import LogLocator, NullFormatter, AutoMinorLocator

# =========================================================
# 1. 색상 팔레트 설정 (lab_style.txt 참고)
# =========================================================
VSET_COLOR = "#D62728"    # Red (after annealing)
VRESET_COLOR = "#2F4EA2"  # Blue (before annealing)
RATIO_COLOR = "#1F4EAA"

# =========================================================
# 2. 폰트 및 기본 그래프 서식 세팅 (lab_style.txt 참고)
# =========================================================
def set_paper_style():
    mpl.rcParams.update({
        "font.family": "Arial",               
        "font.size": 13,                      
        "axes.labelsize": 15,                 
        "axes.titlesize": 16,                 
        "xtick.labelsize": 13,                
        "ytick.labelsize": 13,                
        "legend.fontsize": 11,                
        "axes.linewidth": 1.8,                
        "lines.linewidth": 2.0,               
        "figure.facecolor": "white",          
        "axes.facecolor": "white",            
        "savefig.facecolor": "white",         
        "savefig.dpi": 300,                   
        "xtick.direction": "in",              
        "ytick.direction": "in",              
        "xtick.major.size": 6,                
        "ytick.major.size": 6,                
        "xtick.minor.size": 3,                
        "ytick.minor.size": 3,                
        "xtick.major.width": 1.4,             
        "ytick.major.width": 1.4,             
        "xtick.minor.width": 1.0,             
        "ytick.minor.width": 1.0,             
        "xtick.top": True,                    
        "ytick.right": True,                  
        "legend.frameon": False,              
        "mathtext.fontset": "custom",         
        "mathtext.rm": "Arial",
        "mathtext.it": "Arial:italic",
        "mathtext.bf": "Arial:bold",
        "axes.unicode_minus": False,  # 음수 기호 깨짐 방지
        "svg.fonttype": "none"         # SVG에서 텍스트를 path가 아닌 실제 텍스트로 저장 (일러스트레이터 편집용)
    })

# =========================================================
# 3. 개별 축 디테일 설정 및 로그축 자동 눈금 최적화 함수 (lab_style.txt 참고)
# =========================================================
def format_axes(ax, title=None, xlabel=None, ylabel=None, logx=False, logy=False, is_twin=False):
    if title is not None:
        ax.set_title(title, pad=10)
    if xlabel is not None:
        ax.set_xlabel(xlabel, labelpad=8)
    if ylabel is not None:
        ax.set_ylabel(ylabel, labelpad=8)

    if logx:
        ax.set_xscale("log")
        xmin, xmax = ax.get_xlim()
        if xmin > 0 and xmax > 0:
            xmin_log = 10 ** np.floor(np.log10(xmin))
            xmax_log = 10 ** np.ceil(np.log10(xmax))
            ax.set_xlim(xmin_log, xmax_log)
        ax.xaxis.set_major_locator(LogLocator(base=10.0))
        ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10)))
        ax.xaxis.set_minor_formatter(NullFormatter())
    else:
        if not is_twin:
            ax.xaxis.set_minor_locator(AutoMinorLocator())

    if logy:
        ax.set_yscale("log")
        ymin, ymax = ax.get_ylim()
        if ymin > 0 and ymax > 0:
            ymin_log = 10 ** np.floor(np.log10(ymin))
            ymax_log = 10 ** np.ceil(np.log10(ymax))
            ax.set_ylim(ymin_log, ymax_log)
        ax.yaxis.set_major_locator(LogLocator(base=10.0))
        ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10)))
        ax.yaxis.set_minor_formatter(NullFormatter())
    else:
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    if is_twin:
        ax.tick_params(
            axis="y", which="both", direction="in",
            left=False, labelleft=False, right=True, labelright=True
        )
        ax.tick_params(
            axis="x", which="both", bottom=False, labelbottom=False, top=False, labeltop=False
        )
    else:
        ax.tick_params(
            axis="both", which="both", direction="in",
            left=True, labelleft=True, right=True, labelright=False,
            top=True, labeltop=False
        )
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_linewidth(1.8)

# =========================================================
# 3.1. 단위 변환 및 자동 스케일링 헬퍼 함수
# =========================================================
def get_scale_and_unit(max_val, val_type):
    if val_type == 'current':
        if max_val >= 1e-3:
            return 1e3, 'mA'
        elif max_val >= 1e-6:
            return 1e6, r'$\mu$A'
        elif max_val >= 1e-9:
            return 1e9, 'nA'
        elif max_val >= 1e-12:
            return 1e12, 'pA'
        else:
            return 1e15, 'fA'
    elif val_type == 'capacitance':
        if max_val >= 1e-3:
            return 1e3, 'mF'
        elif max_val >= 1e-6:
            return 1e6, r'$\mu$F'
        elif max_val >= 1e-9:
            return 1e9, 'nF'
        elif max_val >= 1e-12:
            return 1e12, 'pF'
        else:
            return 1e15, 'fF'
    return 1.0, ''

# =========================================================
# 3.2. 실제 데이터 타입 매칭형 출력 파일명 결정 헬퍼 함수
# =========================================================
def get_output_svg_path(file_path, plot_type):
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    name_no_ext, ext = os.path.splitext(base_name)
    name_lower = name_no_ext.lower()
    
    suffix_map = {
        'IV': '_iv',
        'TC': '_tc',
        'CV': '_cv',
        'CF': '_cf',
        'Retention': '_retention',
        'Transient': '_transient',
        'Generic': '_generic'
    }
    target_suffix = suffix_map.get(plot_type, '')
    
    has_correct_suffix = False
    for t_type, suffix in suffix_map.items():
        if suffix in name_lower:
            if t_type == plot_type:
                has_correct_suffix = True
            break
            
    if not has_correct_suffix:
        replaced = False
        for t_type, suffix in suffix_map.items():
            if suffix in name_lower:
                import re
                new_name = re.sub(re.escape(suffix), target_suffix, name_no_ext, flags=re.IGNORECASE)
                name_no_ext = new_name
                replaced = True
                break
        if not replaced and target_suffix:
            name_no_ext = name_no_ext + target_suffix
            
    return os.path.join(dir_name, name_no_ext + '.svg')

# =========================================================
# 4. 파일 타입 자동 분석 판별기 (2단계: 컬럼 구조 우선 + 파일명)
# =========================================================
def classify_and_parse(file_path, df):
    filename = os.path.basename(file_path).lower()
    cols = df.columns.tolist()
    cols_lower = [c.lower() for c in cols]
    
    # 키워드 매칭 도우미
    def find_col(keywords):
        for kw in keywords:
            for idx, c in enumerate(cols_lower):
                if kw == c or (len(kw) > 1 and kw in c):
                    return cols[idx]
        return None

    gatev_col = find_col(['gatev', 'gate_v', 'v_g', 'vg', 'gatevoltage', 'gate voltage'])
    draini_col = find_col(['draini', 'drain_i', 'i_d', 'id', 'draincurrent', 'drain current'])
    gatei_col = find_col(['gatei', 'gate_i', 'i_g', 'ig', 'gatecurrent', 'gate current'])
    
    cap_col = find_col(['capacitance', 'cap', 'c_p', 'c_s', 'cp', 'cs'])
    if not cap_col:
        for idx, c in enumerate(cols_lower):
            if c == 'c':
                cap_col = cols[idx]
                break
                
    volt_col = find_col(['voltage', 'volt', 'v_g', 'vg', 'v_b', 'vb', 'biasv', 'gatev', 'v_d', 'vd'])
    if not volt_col:
        for idx, c in enumerate(cols_lower):
            if c == 'v':
                volt_col = cols[idx]
                break
                
    freq_col = find_col(['frequency', 'freq', 'f', 'hz'])
    time_col = find_col(['time', 't', 'sec', 's'])

    # 1) 출력특성 (Output Curve / IV) - 다중 스윕 (DrainI(1) 등이 존재)
    iv_sweeps = [c for c in cols if c.startswith('DrainI(')]
    if iv_sweeps:
        return {
            'type': 'IV',
            'xlabel': 'Drain Voltage ($V_D$)',
            'ylabel': 'Drain Current ($I_D$)',
            'logx': False,
            'logy': False,
            'title_suffix': 'Output Characteristics'
        }
        
    # 2) 전달특성 (Transfer Curve / TC) - GateV와 DrainI가 존재
    if gatev_col and draini_col:
        return {
            'type': 'TC',
            'x_col': gatev_col,
            'y_cols': [draini_col] + ([gatei_col] if gatei_col else []),
            'xlabel': 'Gate Voltage ($V_G$)',
            'ylabel': 'Current (A)',
            'logx': False,
            'logy': True,
            'title_suffix': 'Transfer Characteristics'
        }
        
    # 3) C-V (Capacitance-Voltage) - Capacitance와 Voltage 존재
    if cap_col and volt_col and not freq_col:
        xlbl = 'Gate Voltage ($V_G$)' if 'gate' in volt_col.lower() or 'vg' in volt_col.lower() else 'Voltage (V)'
        return {
            'type': 'CV',
            'x_col': volt_col,
            'y_cols': [cap_col],
            'xlabel': xlbl,
            'ylabel': 'Capacitance (F)',
            'logx': False,
            'logy': False,
            'title_suffix': 'Capacitance-Voltage (C-V)'
        }
        
    # 4) C-f (Capacitance-Frequency) - Capacitance와 Frequency 존재
    if cap_col and freq_col:
        return {
            'type': 'CF',
            'x_col': freq_col,
            'y_cols': [cap_col],
            'xlabel': 'Frequency (Hz)',
            'ylabel': 'Capacitance (F)',
            'logx': True,
            'logy': False,
            'title_suffix': 'Capacitance-Frequency (C-f)'
        }

    # 5) 시간 기반 측정 (Retention / Stability / Pulse Stress / Read Current 등)
    if time_col:
        y_cols = [c for c in cols if c != time_col and not c.startswith('Time.1')]
        
        # Y라벨 정교화
        if len(y_cols) == 1:
            y_name = y_cols[0].lower()
            if 'draini' in y_name or 'id' in y_name:
                ylbl = 'Drain Current ($I_D$)'
            elif 'gatei' in y_name or 'ig' in y_name:
                ylbl = 'Gate Current ($I_G$)'
            elif 'current' in y_name or y_name == 'i':
                ylbl = 'Current (A)'
            elif 'cap' in y_name or y_name == 'c':
                ylbl = 'Capacitance (F)'
            else:
                ylbl = y_cols[0]
        else:
            if all('current' in c.lower() or 'i' in c.lower() for c in y_cols):
                ylbl = 'Current (A)'
            else:
                ylbl = 'Value'
                
        # 파일명 기반으로 세부 구분
        if "retention" in filename:
            return {
                'type': 'Retention',
                'x_col': time_col,
                'y_cols': y_cols,
                'xlabel': 'Time (s)',
                'ylabel': ylbl,
                'logx': True,
                'logy': False,
                'title_suffix': 'Retention Characteristics'
            }
        
        t_suffix = 'Transient Characteristics'
        if 'stability' in filename:
            t_suffix = 'Stability Characteristics'
        elif 'pulse_stress' in filename:
            t_suffix = 'Pulse Stress'
        elif 'read_current' in filename:
            t_suffix = 'Read Current'
        elif 'program' in filename:
            t_suffix = 'Program Transient'
            
        return {
            'type': 'Transient',
            'x_col': time_col,
            'y_cols': y_cols,
            'xlabel': 'Time (s)',
            'ylabel': ylbl,
            'logx': False,
            'logy': False,
            'title_suffix': t_suffix
        }

    # 6) 파일명 매핑 기반 판별 (컬럼이 애매할 경우 파일명으로 유추)
    if "_tc_" in filename or "transfer" in filename:
        gatev_col = cols[0]
        draini_col = cols[1] if len(cols) > 1 else cols[0]
        return {
            'type': 'TC',
            'x_col': gatev_col,
            'y_cols': [draini_col],
            'xlabel': 'Gate Voltage ($V_G$)',
            'ylabel': 'Current (A)',
            'logx': False,
            'logy': True,
            'title_suffix': 'Transfer Characteristics'
        }
        
    if "_iv_" in filename or "output" in filename:
        return {
            'type': 'Generic',
            'x_col': cols[0],
            'y_cols': cols[1:],
            'xlabel': 'Voltage (V)',
            'ylabel': 'Current (A)',
            'logx': False,
            'logy': False,
            'title_suffix': 'Output Characteristics'
        }

    # 7) 기본 폴백
    return {
        'type': 'Generic',
        'x_col': cols[0],
        'y_cols': cols[1:],
        'xlabel': cols[0],
        'ylabel': 'Value',
        'logx': False,
        'logy': False,
        'title_suffix': 'Measured Data'
    }

# =========================================================
# 5. 파일 변환 프로세스
# =========================================================
def process_file(file_path):
    print(f"\nProcessing: {file_path}")
    
    lower_path = file_path.lower()
    
    # 샘플명 파악 (경로 전체에서 검색)
    sample_name = None
    if "sample 1" in lower_path or "sample1" in lower_path:
        sample_name = "Sample 1"
    elif "sample 2" in lower_path or "sample2" in lower_path:
        sample_name = "Sample 2"
    elif "sample 3" in lower_path or "sample3" in lower_path:
        sample_name = "Sample 3"
    elif "thinner" in lower_path:
        sample_name = "Thinner MoS2"
    else:
        import re
        match = re.search(r'sample\s*(\d+)', lower_path)
        if match:
            sample_name = f"Sample {match.group(1)}"
        else:
            # 매칭되는 샘플명이 없으면 파일명 앞부분 활용 (_before, _after, _tc, _iv 등을 대소문자 무시하고 제거)
            base_name_no_ext = os.path.splitext(os.path.basename(file_path))[0]
            cleaned = base_name_no_ext
            for suffix in ['_before', '_after', '_heating', '_150c', '_tc', '_iv', '_cv', '_cf', '_retention', '_transient', '_generic']:
                if cleaned.lower().endswith(suffix):
                    cleaned = cleaned[:-len(suffix)]
            cleaned = cleaned.rstrip('_-')
            sample_name = cleaned if cleaned else "Sample 1"

    # 어닐링 상태 파악 (경로 전체에서 검색)
    is_after = False
    if "after" in lower_path or "heating" in lower_path or "150c" in lower_path:
        if "before" not in lower_path:
            is_after = True
            
    annealing_status = "After Annealing" if is_after else "Before Annealing"
    base_color = VSET_COLOR if is_after else VRESET_COLOR
    
    # 엑셀 데이터 로드
    df = pd.read_excel(file_path)
    
    # 분류기 실행
    info = classify_and_parse(file_path, df)
    
    # 그래프 객체 생성
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # 타이틀 생성
    title = f"{sample_name} - {info['title_suffix']}\n({annealing_status})"
    plot_type = info['type']
    
    # Determine value type for scaling
    val_type = 'other'
    if plot_type in ['TC', 'IV']:
        val_type = 'current'
    elif plot_type in ['CV', 'CF']:
        val_type = 'capacitance'
    else:
        yl_lower = info['ylabel'].lower()
        if 'current' in yl_lower or 'i' in yl_lower:
            val_type = 'current'
        elif 'capacitance' in yl_lower or 'cp' in yl_lower or 'cs' in yl_lower:
            val_type = 'capacitance'

    # Auto-scaling logic (only if not log y-axis)
    scale = 1.0
    unit_suffix = ''
    if not info['logy'] and val_type in ['current', 'capacitance']:
        if plot_type == 'IV':
            iv_cols = [c for c in df.columns if c.startswith('DrainI(')]
            if iv_cols:
                max_val = df[iv_cols].abs().max().max()
            else:
                max_val = 0.0
        else:
            y_cols = info['y_cols']
            if y_cols:
                max_val = df[y_cols].abs().max().max()
            else:
                max_val = 0.0
        
        if not np.isnan(max_val) and max_val > 0:
            scale, unit_suffix = get_scale_and_unit(max_val, val_type)

    # Format Y-label with scaled units
    ylabel_str = info['ylabel']
    if unit_suffix:
        if '(A)' in ylabel_str:
            ylabel_str = ylabel_str.replace('(A)', f'({unit_suffix})')
        elif '(F)' in ylabel_str:
            ylabel_str = ylabel_str.replace('(F)', f'({unit_suffix})')
        else:
            ylabel_str = f"{ylabel_str} ({unit_suffix})"
    else:
        # Default unit if not scaled
        if val_type == 'current' and not any(u in ylabel_str for u in ['(A)', '(mA)', '(uA)', '(nA)', '(pA)', '(fA)', r'(\mu A)']):
            ylabel_str = f"{ylabel_str} (A)"
        elif val_type == 'capacitance' and not any(u in ylabel_str for u in ['(F)', '(mF)', '(uF)', '(nF)', '(pF)', '(fF)', r'(\mu F)']):
            ylabel_str = f"{ylabel_str} (F)"

    if plot_type == 'TC':
        x_col = info['x_col']
        y_drain = info['y_cols'][0]
        
        if len(info['y_cols']) > 1:
            y_gate = info['y_cols'][1]
            # Left axis: Drain Current (I_D) (clipped to avoid log10(0) error)
            y_drain_data = np.clip(np.abs(df[y_drain]), 1e-15, None)
            line1 = ax.plot(df[x_col], y_drain_data * scale, color=base_color, label='Drain Current ($I_D$)', linewidth=2.0)
            
            # Right axis: Gate Current (I_G) (clipped to avoid log10(0) error)
            ax2 = ax.twinx()
            y_gate_data = np.clip(np.abs(df[y_gate]), 1e-15, None)
            line2 = ax2.plot(df[x_col], y_gate_data * scale, color='#7F7F7F', linestyle='--', label='Gate Current ($I_G$)', linewidth=1.5)
            
            unit_str = unit_suffix if unit_suffix else 'A'
            ylabel_left = f'Drain Current ($I_D$) ({unit_str})'
            ylabel_right = f'Gate Current ($I_G$) ({unit_str})'
            
            # Format axes
            format_axes(ax, title=title, xlabel=info['xlabel'], ylabel=ylabel_left, logx=info['logx'], logy=info['logy'])
            format_axes(ax2, ylabel=ylabel_right, logy=info['logy'], is_twin=True)
            
            # Combine legends
            lines = line1 + line2
            labels = [l.get_label() for l in lines]
            ax.legend(lines, labels, loc='best')
        else:
            # Single Y-axis (clipped to avoid log10(0) error)
            y_drain_data = np.clip(np.abs(df[y_drain]), 1e-15, None)
            ax.plot(df[x_col], y_drain_data * scale, color=base_color, label='Drain Current ($I_D$)', linewidth=2.0)
            format_axes(ax, title=title, xlabel=info['xlabel'], ylabel=ylabel_str, logx=info['logx'], logy=info['logy'])
            ax.legend(loc='best')
        
    elif plot_type == 'IV':
        columns = df.columns.tolist()
        num_sweeps = sum(1 for col in columns if col.startswith('DrainI('))
        
        if is_after:
            colors = [plt.cm.Reds(x) for x in np.linspace(0.4, 0.95, num_sweeps)]
        else:
            colors = [plt.cm.Blues(x) for x in np.linspace(0.4, 0.95, num_sweeps)]
            
        for i in range(1, num_sweeps + 1):
            i_col = f"DrainI({i})"
            v_col = f"DrainV({i})"
            g_col = f"GateV({i})"
            
            if i_col in df.columns and v_col in df.columns:
                vg_val = df[g_col].iloc[0] if g_col in df.columns else None
                label_str = f"$V_G$ = {vg_val:.0f} V" if vg_val is not None else f"Sweep {i}"
                ax.plot(df[v_col], df[i_col] * scale, color=colors[i-1], label=label_str, linewidth=1.8)
                
        format_axes(ax, title=title, xlabel=info['xlabel'], ylabel=ylabel_str, logx=info['logx'], logy=info['logy'])
        ax.legend(loc='best', fontsize=8.5, ncol=2)
        
    else:
        # CV, CF, Retention, Transient, Generic 공통 그리기
        x_col = info['x_col']
        y_cols = info['y_cols']
        
        if len(y_cols) == 1:
            y_col = y_cols[0]
            label_name = 'ON State ($I_D$)' if plot_type == 'Retention' else y_col
            ax.plot(df[x_col], df[y_col] * scale, color=base_color, label=label_name, linewidth=2.0)
        else:
            if is_after:
                colors = [plt.cm.Reds(x) for x in np.linspace(0.4, 0.95, len(y_cols))]
            else:
                colors = [plt.cm.Blues(x) for x in np.linspace(0.4, 0.95, len(y_cols))]
                
            for idx, y_col in enumerate(y_cols):
                ax.plot(df[x_col], df[y_col] * scale, color=colors[idx], label=y_col, linewidth=1.8)
                
        format_axes(ax, title=title, xlabel=info['xlabel'], ylabel=ylabel_str, logx=info['logx'], logy=info['logy'])
        ax.legend(loc='best')

    plt.tight_layout()
    
    # SVG 저장
    svg_path = get_output_svg_path(file_path, plot_type)
    plt.savefig(svg_path, format='svg', bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {svg_path}")

# =========================================================
# 6. 메인 실행 함수
# =========================================================
def main():
    set_paper_style()
    
    # 1. 실행 경로 결정 (인자로 넘겨받거나 현재 디렉토리 기준)
    if len(sys.argv) > 1:
        search_dir = os.path.abspath(sys.argv[1])
    else:
        search_dir = os.getcwd()
    
    # 재귀적으로 모든 xls/xlsx 파일 찾기
    pattern = os.path.join(search_dir, "**", "*.xls*")
    files = glob.glob(pattern, recursive=True)
    
    # .DS_Store 나 임시 파일 등 제외하고 정렬
    valid_files = sorted([f for f in files if os.path.isfile(f) and not os.path.basename(f).startswith("~$") and os.path.splitext(f)[1] in [".xls", ".xlsx"]])
    
    print(f"Found {len(valid_files)} Excel files to convert.")
    
    for f in valid_files:
        try:
            process_file(f)
        except Exception as e:
            print(f"Error processing {f}: {e}")

if __name__ == "__main__":
    main()
