# vue + BootstrapVue

## day01
### 建立vue项目
```
vue init webpack frontend
```

### 安装BootstrapVue
#### 下载BootstrapVue
```
# With npm
npm install vue bootstrap-vue bootstrap
```
#### 配置BootstrapVue
打开src/main.js文件
```
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

// 引入样式文件
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
```
# nginx
## 1. 安装nginx
```shell
sudo su root

apt-get install nginx
```
## 2.查看是否安装成功
```shell
nginx -v
```
启动后 可在浏览器查看服务器IP，显示nginx则安装成功
## 3. nginx命令
```shell
nginx -s start # 启动
nginx -s reload # 重启
nginx -s stop # 停止

whereis nginx # 查看nginx安装位置，一般为/etc/nginx
```
## 4. 修改nginx目录下 nginx.conf文件
```
server {
        listen       8088; # 端口
        server_name  101.200.40.217; # 服务器ip
        location / {
            root /home/project/MU3DSP/frontend/dist; # 打包后的项目位置
            index  index.html index.htm;
        }
        location /api {
            proxy_pass   http://101.200.40.217:5000; # 后端端口 所有/api都被转到http://101.200.40.217:5000
        }
        error_page   404  /404.html; # 404界面
        location = /404.html {
            root   html;
        }
        error_page   500 502 503 504  /50x.html; # 50x界面
        location = /50x.html {
            root   html;
        }
    }
```

