// 图片处理工具函数

/**
 * 处理动漫封面图片URL
 * - 优先使用数据库中的原图
 * - 提供可靠的占位图作为兜底
 */
export function getAnimeCoverImage(anime: any): string {
  const originalUrl = anime.cover_image;
  
  // 如果没有图片URL，返回占位图
  if (!originalUrl || originalUrl.trim() === '') {
    return getPlaceholderImage(anime);
  }
  
  // 检查URL协议
  if (originalUrl.startsWith('http://')) {
    // HTTP图片可能在HTTPS环境下被阻止，尝试转换为HTTPS
    const httpsUrl = originalUrl.replace('http://', 'https://');
    return httpsUrl;
  }
  
  // 优先返回数据库中的原图
  return originalUrl;
}

/**
 * 获取占位图
 */
export function getPlaceholderImage(anime: any): string {
  // 使用picsum.photos，用动漫ID或标题作为seed
  const seed = anime.title ? encodeURIComponent(anime.title) : `anime-${anime.id}`;
  return `https://picsum.photos/seed/${seed}/300/400`;
}

/**
 * 获取渐变背景色（用于占位）
 */
export function getGradientColor(anime: any): string {
  const colors = [
    'linear-gradient(135deg, #ff6b9d 0%, #c44cff 100%)',
    'linear-gradient(135deg, #00d4ff 0%, #0099ff 100%)',
    'linear-gradient(135deg, #7cff7c 0%, #00cc88 100%)',
    'linear-gradient(135deg, #ffd700 0%, #ff8c00 100%)',
    'linear-gradient(135deg, #ff8c00 0%, #ff4444 100%)',
    'linear-gradient(135deg, #c44cff 0%, #00d4ff 100%)',
    'linear-gradient(135deg, #ff6b9d 0%, #ffd700 100%)',
    'linear-gradient(135deg, #00cc88 0%, #00d4ff 100%)'
  ];
  const index = anime.id % colors.length;
  return colors[index];
}

/**
 * 验证图片URL是否有效
 */
export function isValidImageUrl(url: string): boolean {
  if (!url || url.trim() === '') return false;
  
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}
