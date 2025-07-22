import matplotlib.pyplot as plt
import numpy as np

# Data preparation
applications = ['Jellyfin', 'Appwrite', 'Casdoor', 'HttPlaceholder']
lira_core_coverage = [38.26, 83.16, 96.70, 51.43]
lira_nospec_coverage = [28.98, 55.79, 80.99, 22.86]

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False
bar_width = 0.35
x = np.arange(len(applications))

plt.figure(figsize=(10, 6))

# 使用你提供的RGB颜色，转换为Matplotlib可识别的0-1浮点格式
color1 = (255/255, 244/255, 242/255)  # #FFF4F2
color2 = (254/255, 179/255, 174/255)  # #FEB3AE

plt.bar(x - bar_width/2, lira_core_coverage, width=bar_width,
        label='LIRA-Basic', color=color1, edgecolor='black')
plt.bar(x + bar_width/2, lira_nospec_coverage, width=bar_width,
        label='LIRA-NoSpec', color=color2, edgecolor='black')

plt.xlabel('Tested Applications', fontsize=12, weight='bold')
plt.ylabel('Endpoint Coverage (%)', fontsize=12, weight='bold')
plt.title('Endpoint Coverage Comparison: LIRA-Basic vs LIRA-NoSpec', fontsize=14, weight='bold')
plt.xticks(x, applications, fontsize=11)
plt.ylim(0, 110)

for i in range(len(applications)):
    plt.text(x[i] - bar_width/2, lira_core_coverage[i] + 2,
             f'{lira_core_coverage[i]:.2f}%', ha='center', fontsize=10)
    plt.text(x[i] + bar_width/2, lira_nospec_coverage[i] + 2,
             f'{lira_nospec_coverage[i]:.2f}%', ha='center', fontsize=10)

plt.legend(loc='upper right', fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('coverage_comparison_updated.png', dpi=300)
plt.show()
