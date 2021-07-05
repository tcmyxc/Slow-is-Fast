<center><font size="48px"><b>JavaWeb</b></font></center>

# Servlet

## 简介

Servlet（Server Applet）是[Java](https://baike.baidu.com/item/Java/85979) Servlet的简称，称为小服务程序或服务连接器，用Java编写的[服务器](https://baike.baidu.com/item/服务器/100571)端程序，具有独立于平台和[协议](https://baike.baidu.com/item/协议/13020269)的特性，主要功能在于交互式地浏览和生成数据，生成动态[Web](https://baike.baidu.com/item/Web/150564)内容。

广义的Servlet是指任何实现了Servlet接口的类

Servlet运行于支持Java的应用服务器中。从原理上讲，Servlet可以响应任何类型的请求，但绝大多数情况下Servlet只用来扩展基于HTTP协议的Web服务器。

【总结】实现了servlet接口的java程序，就是servlet

## HelloServlet

Servlet接口Sun公司有两个默认的实现类：HttpServlet，GenericServlet

1. maven模板，webapp，修改web.xml（这部分看自己tomcat服务器web.xml是啥，然后复制个头文件过来就行）

   ```xml
   <?xml version="1.0" encoding="UTF-8" ?>
   <web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                         http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
            version="4.0"
            metadata-complete="true">
   
     
   </web-app>
   ```

   

2. 将项目的结构补充完整，java和resources

   ![image-20210620151553413](../images/image-20210620151553413.png)

   

3. 编写一个Servlet程序

   - 编写一个普通的类

   - 实现Servlet接口，这里我们直接继承HttpServlet

     ```java
     public class HelloServlet extends HttpServlet {
     
         // 由于get或者post只是实现方式不同，可以互相调用，业务逻辑都一样
         @Override
         protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
             PrintWriter writer = resp.getWriter();
     
             writer.print("Hello Servlet!");
         }
     
         @Override
         protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
             doGet(req, resp);
         }
     }
     ```

4. 编写Servlet的映射

   - 为什么需要映射？

     - 因为我们写的是java程序，但是要通过浏览器访问，浏览器访问需要连接服务器，所以我们需要在web服务中注册我们写的Servlet，还需要给个URL路径

       ```xml
       <!--注册servlet-->
       <servlet>
           <servlet-name>hello</servlet-name>
           <servlet-class>com.tcmyxc.servlet.HelloServlet</servlet-class>
       </servlet>
       <!--servlet请求路径-->
       <servlet-mapping>
           <servlet-name>hello<</servlet-name>
               <url-pattern>/hello</url-pattern>
       </servlet-mapping>
       ```

       

5. 配置Tomcat

   - 注意配置项目发布的路径

   ![image-20210620153251176](../images/image-20210620153251176.png)

6. 启动测试



## Servlet原理

Servlet由Web服务器调用

![image-20210620150127559](../images/image-20210620150127559.png)









































