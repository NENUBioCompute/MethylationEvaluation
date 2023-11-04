x <- c(1,2,3,4)
y <- x*x
jpeg(file= "plot.jpg") # 保存图像
plt <- plot(x,y) # 画散点图
dev.off() # 关闭设备
