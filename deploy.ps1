$server = "59.110.214.50"
$user = "root"
$password = "Xinmima1109"

# 安装 Posh-SSH 模块
if (-not (Get-Module -ListAvailable -Name Posh-SSH)) {
    Install-Module -Name Posh-SSH -Force -Scope CurrentUser
}

# 导入模块
Import-Module Posh-SSH

# 创建凭证
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential ($user, $securePassword)

try {
    # 建立SSH连接
    $session = New-SSHSession -ComputerName $server -Credential $credential -AcceptKey
    
    if ($session.Connected) {
        Write-Host "SSH连接成功！"
        
        # 执行命令测试
        $result = Invoke-SSHCommand -SSHSession $session -Command "echo '连接成功' && whoami && pwd && cat /etc/os-release"
        Write-Host $result.Output
        
        # 关闭会话
        Remove-SSHSession -SSHSession $session
    }
}
catch {
    Write-Host "连接失败: $_"
}
