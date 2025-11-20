# EnableZuulProxy 注解是如何生效的？

使用 zuul 网关的时候，我们会在启动类上加一个 `@EnableZuulProxy`，本文解析一下该注解是如何起作用的。

注解源码：

```java
@EnableCircuitBreaker
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Import(ZuulProxyMarkerConfiguration.class)
public @interface EnableZuulProxy {

}
```



源码上的 `@Import(ZuulProxyMarkerConfiguration.class)` 表明要导入 `ZuulProxyMarkerConfiguration`，我们看一下这个类的源码：

```java
@Configuration
public class ZuulProxyMarkerConfiguration {

	@Bean
	public Marker zuulProxyMarkerBean() {
		return new Marker();
	}

	class Marker {

	}

}
```



可以看到，`ZuulProxyMarkerConfiguration` 这个类会自动注入一个类 `Marker`，也就是说，注解`@EnableZuulProxy` 会注入一个类 `Marker`。

然后我们看对应的配置类 `ZuulProxyAutoConfiguration`：

```java
@Configuration
@Import({ RibbonCommandFactoryConfiguration.RestClientRibbonConfiguration.class,
		RibbonCommandFactoryConfiguration.OkHttpRibbonConfiguration.class,
		RibbonCommandFactoryConfiguration.HttpClientRibbonConfiguration.class,
		HttpClientConfiguration.class })
@ConditionalOnBean(ZuulProxyMarkerConfiguration.Marker.class)
public class ZuulProxyAutoConfiguration extends ZuulServerAutoConfiguration 
```



可以看到，这个类上面有个条件注解 `@ConditionalOnBean(ZuulProxyMarkerConfiguration.Marker.class)`。也就是说，仅当 Bean 工厂中存在类 `Marker` 时，该配置类才会被自动注入。



**为什么用 Marker 而不是直接 Import AutoConfiguration？** 

这是一种显式开关做法：通过注解导入一个小的 marker bean，然后让自动配置用  `@ConditionalOnBean` 检测该 marker，从而在需要时启用完整的自动配置，而不依赖于类路径扫描或 `spring.factories` 的被动触发。不必在 `application.properties` 中强制添加配置才能生效，适合明确的“按注解启用”场景。