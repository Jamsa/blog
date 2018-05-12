Title: Maven2 Tips
Date: 2009-09-21
Modified: 2009-09-21
Category: 开发
Tags: maven

# mvn命令行
## 执行Java程序
```
mvn exec:java -Dexec.mainClass=org.jamsa.scalademo.FunctionValue
```

## 运行单个单元测试
```
mvn test -Dtest=AppTest
```

## 安装包和源码包
```
mvn install:install-file -Dfile=target/jsonplugin-0.34.jar -Dsources=target/jsonplugin-0.34-sources.jar -DartifactId=jsonplugin -DgroupId=com.googlecode -Dversion=0.34 -Dclassifier=sources -Dpackaging=jar
```

## 生成lift应用
```
mvn.bat archetype:generate -U -DarchetypeGroupId=net.liftweb -DarchetypeArtifactId=lift-archetype-blank -DremoteRepositories=http://scala-tools.org/repo-releases -DgroupId=demo.helloworld -DartifactId=helloworld -Dversion=1.0-SNAPSHOT
```

# pom.xml配置

## dependency的scope
```xml
	<dependency>
		<groupId>junit</groupId>
		<artifactId>junit</artifactId>
		<version>3.8.1</version>
		<scope>test</scope>
	</dependency>
	<!-- 使ide能找到c标签库的tld文件 -->
	<dependency>
		<groupId>taglibs</groupId>
		<artifactId>standard</artifactId>
		<version>1.1.2</version>
		<scope>provided</scope>
	</dependency>
```
这里的test表示在测试时才需要该依赖。而provided则表示发布后的环境中将提供这个包。

## scala插件配置
```xml
      <plugin>
        <groupId>org.scala-tools</groupId>
        <artifactId>maven-scala-plugin</artifactId>
        <executions>
          <execution>
            <goals>
              <goal>compile</goal>
              <goal>testCompile</goal>
            </goals>
          </execution>
        </executions>
        <configuration>
          <scalaVersion>${scala.version}</scalaVersion>
          <args>
            <arg>-target:jvm-1.5</arg>
            <arg>-encoding</arg>
            <arg>GBK</arg>
          </args>
        </configuration>
      </plugin>
```
通过args可指定-encoding参数，可以避免出现scalac识别源码字符集错误的问题。

## 指定所使用的依赖的编译版本
```xml
	<dependency>
		<groupId>org.json</groupId>
		<artifactId>json</artifactId>
		<version>20090211</version>
		<classifier>jdk1.5</classifier>
	</dependency>
```

## jetty插件的配置
```xml
        <plugin>
		<groupId>org.mortbay.jetty</groupId>
		<artifactId>maven-jetty-plugin</artifactId>
		<configuration>
			<stopPort>9966</stopPort>
			<stopKey>foo</stopKey>
			<webAppConfig>
				<contextPath>/budget</contextPath>
				<defaultsDescriptor>src/main/resources/webdefault.xml
				</defaultsDescriptor>
				<!--
					<overrideDescriptor>src/main/resources/override-web.xml</overrideDescriptor>
				-->
			</webAppConfig>
		</configuration>
	</plugin>
```
这里有一个样例 [webdefault.xml](webdefault.xml) 。webdefault.xml可以解决执行jetty:run时静态文件不能修改的问题。

## 一个简单的Profile
```xml
	<profiles>
		<profile>
			<id>oc4j</id>
			<dependencies>
				<dependency>
					<groupId>xerces</groupId>
					<artifactId>xercesImpl</artifactId>
					<version>2.6.2</version>
				</dependency>
				<dependency>
					<groupId>javax.servlet</groupId>
					<artifactId>jstl</artifactId>
					<version>1.1.2</version>
				</dependency>
				<dependency>
					<groupId>taglibs</groupId>
					<artifactId>standard</artifactId>
					<version>1.1.2</version>
				</dependency>
			</dependencies>
			<build>
				<plugins>
					<plugin>
						<artifactId>maven-war-plugin</artifactId>
						<configuration>
							<webResources>
								<resource>
									<directory>src/main/oc4j</directory>
								</resource>
							</webResources>
						</configuration>
					</plugin>
				</plugins>
			</build>
		</profile>
	</profiles>
```
