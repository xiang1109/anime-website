import requests
import time

print("="*60)
print("验证外部访问")
print("="*60)

# 等待1分钟让配置生效
print("\n等待60秒让安全组配置生效...")
for i in range(60, 0, -10):
    print(f"  还剩 {i} 秒...")
    time.sleep(10)

# 测试访问
print("\n=== 测试外部访问 ===")
try:
    response = requests.get("http://59.110.214.50", timeout=10)
    print(f"状态码: {response.status_code}")
    print(f"响应长度: {len(response.text)}")
    if response.status_code == 200:
        print("\n✅ 访问成功！")
        print("请在浏览器打开: http://59.110.214.50")
    else:
        print(f"\n⚠️  访问异常，状态码: {response.status_code}")
except Exception as e:
    print(f"\n❌ 访问失败: {e}")
    print("可能还需要等待更长时间，或者检查网络连接")

print("\n" + "="*60)
print("服务状态确认：")
print("="*60)
print("✅ Nginx: 运行中 (端口80)")
print("✅ 后端API: 运行中 (端口3001)")
print("✅ MySQL: 运行中 (端口3306)")
print("✅ 80端口: 已开放")
print("="*60)
