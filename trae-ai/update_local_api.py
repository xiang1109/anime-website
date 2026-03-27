import os
import re

# 定义要修改的文件列表
files_to_update = [
    'src/pages/AdminPage.tsx',
    'src/components/RegisterModal.tsx',
    'src/pages/SearchPage.tsx',
    'src/components/LoginModal.tsx',
    'src/components/AnimeDetailModal.tsx',
]

# 替换规则
replacements = [
    ("http://localhost:3001", ""),
]

print("="*60)
print("更新本地代码中的API地址")
print("="*60)

for file_path in files_to_update:
    if os.path.exists(file_path):
        print(f"\n处理文件: {file_path}")
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 执行替换
        for old_str, new_str in replacements:
            content = content.replace(old_str, new_str)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path} 已更新")
    else:
        print(f"❌ {file_path} 不存在")

print("\n" + "="*60)
print("所有文件更新完成！")
print("="*60)
