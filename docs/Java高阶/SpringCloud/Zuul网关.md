场景：eureka 注册中心上显示的服务名为全大写，但是通过zuul网关调用的时候，服务名要全小写

Eureka 

在 `com.netflix.appinfo.InstanceInfo.Builder#setAppName(String)` 方法中，源码如下：

```java
public Builder setAppName(String appName) {
    result.appName = intern.apply(appName.toUpperCase(Locale.ROOT));
    return this;
}
```

这说明，当服务注册到 Eureka 时，其 `appName`（即服务名）会被强制转为大写形式。



Zuul 

在 `org.springframework.cloud.netflix.eureka.EurekaDiscoveryClient#getServices` 方法中，从注册中心拿到服务之后，spring 会手动把服务名转换为全小写

```java
@Override
public List<String> getServices() {
    Applications applications = this.eurekaClient.getApplications();
    if (applications == null) {
        return Collections.emptyList();
    }
    List<Application> registered = applications.getRegisteredApplications();
    List<String> names = new ArrayList<>();
    for (Application app : registered) {
        if (app.getInstances().isEmpty()) {
            continue;
        }
        names.add(app.getName().toLowerCase());

    }
    return names;
}
```



这也就是为什么 `http://127.0.0.1:9528/cloud-payment-service/payment/get/1` 访问成功，但是服务名大写 `http://127.0.0.1:9528/CLOUD-PAYMENT-SERVICE/payment/get/1` 报404的原因