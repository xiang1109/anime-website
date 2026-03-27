import { useState, useEffect } from 'react';

const YourNameSection: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // 当组件挂载时，设置可见性为true，触发动画
    setIsVisible(true);
  }, []);

  return (
    <section className="py-16 bg-gradient-to-r from-blue-900 to-purple-900 relative overflow-hidden">
      {/* 背景装饰 */}
      <div className="absolute top-0 left-0 w-full h-full opacity-20">
        <div className="absolute top-20 left-10 w-20 h-20 bg-white rounded-full filter blur-3xl"></div>
        <div className="absolute bottom-20 right-10 w-32 h-32 bg-pink-500 rounded-full filter blur-3xl"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-40 h-40 bg-blue-500 rounded-full filter blur-3xl"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className={`transition-all duration-1000 ease-out transform ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">秒速五厘米</h2>
            <p className="text-lg text-blue-100 max-w-3xl mx-auto">
              樱花飘落的速度是每秒五厘米，那么我要以怎样的速度，才能与你相遇？
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            {/* 左侧图片 */}
            <div className="relative">
              <div className="aspect-w-4 aspect-h-3 overflow-hidden rounded-2xl shadow-2xl">
                <img 
                  src="https://cdn.myanimelist.net/images/anime/11/19844.jpg" 
                  alt="秒速五厘米" 
                  className="object-cover w-full h-full transition-transform duration-700 hover:scale-105"
                />
              </div>
              <div className="absolute -bottom-4 -right-4 bg-pink-600 text-white px-6 py-2 rounded-full shadow-lg">
                <span className="font-semibold">新海诚作品</span>
              </div>
            </div>

            {/* 右侧内容 */}
            <div className="space-y-6">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <h3 className="text-2xl font-semibold text-white mb-4">关于这部作品</h3>
                <p className="text-blue-100 mb-4">
                  《秒速五厘米》是新海诚执导的动画电影，讲述了远野贵树和筱原明里之间跨越时间和距离的爱情故事。
                  影片以樱花、火车、星空等元素营造出唯美而忧伤的氛围，展现了青春的遗憾与成长。
                </p>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-blue-300 text-sm">上映时间</p>
                    <p className="text-white font-medium">2007年</p>
                  </div>
                  <div>
                    <p className="text-blue-300 text-sm">类型</p>
                    <p className="text-white font-medium">爱情、青春</p>
                  </div>
                  <div>
                    <p className="text-blue-300 text-sm">导演</p>
                    <p className="text-white font-medium">新海诚</p>
                  </div>
                  <div>
                    <p className="text-blue-300 text-sm">片长</p>
                    <p className="text-white font-medium">63分钟</p>
                  </div>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <a 
                  href="/search?keyword=秒速五厘米" 
                  className="flex-1 bg-white text-blue-900 hover:bg-blue-100 transition-colors font-medium py-3 px-6 rounded-lg text-center"
                >
                  查看详情
                </a>
                <a 
                  href="/search?keyword=新海诚" 
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white transition-colors font-medium py-3 px-6 rounded-lg text-center"
                >
                  探索更多新海诚作品
                </a>
              </div>
            </div>
          </div>

          {/* 樱花飘落动画 */}
          <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
            {[...Array(20)].map((_, i) => (
              <div 
                key={i}
                className="absolute bg-pink-200 rounded-full opacity-70"
                style={{
                  width: `${Math.random() * 10 + 5}px`,
                  height: `${Math.random() * 10 + 5}px`,
                  left: `${Math.random() * 100}%`,
                  top: `-20px`,
                  animation: `fall ${Math.random() * 10 + 10}s linear ${Math.random() * 5}s infinite`,
                }}
              />
            ))}
          </div>
        </div>
      </div>


    </section>
  );
};

export default YourNameSection;
