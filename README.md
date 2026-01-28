# HospitalManagementSystem
## Here I will add my files on Hotel Management System for frontend backend and other required fields
# MediCare Hospital - JavaFX Application

A hospital homepage application built with JavaFX, featuring login/signup functionality, department listings, and real-time clock display.

## Features

- **Real-time Clock**: Displays current time and date with live updates
- **Department Navigation**: Six main departments (Cardiology, Neurology, Orthopedics, Pediatrics, Emergency, Radiology)
- **Login/Signup System**: Toggle between login and signup modes
- **Responsive Design**: Clean, modern interface with gradient backgrounds
- **About Section**: Information about the hospital
- **Footer**: Contact information, emergency services, and operating hours

## Prerequisites

- Java Development Kit (JDK) 11 or higher
- JavaFX SDK 11 or higher

## Installation

### Option 1: Using JavaFX SDK

1. Download JavaFX SDK from [https://gluonhq.com/products/javafx/](https://gluonhq.com/products/javafx/)

2. Compile the application:
```bash
javac --module-path /path/to/javafx-sdk/lib --add-modules javafx.controls HospitalHomepage.java
```

3. Run the application:
```bash
java --module-path /path/to/javafx-sdk/lib --add-modules javafx.controls HospitalHomepage
```

### Option 2: Using Maven

Create a `pom.xml` file with JavaFX dependencies:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.medicare</groupId>
    <artifactId>hospital-homepage</artifactId>
    <version>1.0</version>
    
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.openjfx</groupId>
            <artifactId>javafx-controls</artifactId>
            <version>19</version>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.openjfx</groupId>
                <artifactId>javafx-maven-plugin</artifactId>
                <version>0.0.8</version>
                <configuration>
                    <mainClass>HospitalHomepage</mainClass>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

Then run:
```bash
mvn clean javafx:run
```

### Option 3: Using Gradle

Create a `build.gradle` file:

```groovy
plugins {
    id 'application'
    id 'org.openjfx.javafxplugin' version '0.0.13'
}

javafx {
    version = "19"
    modules = [ 'javafx.controls' ]
}

application {
    mainClass = 'HospitalHomepage'
}
```

Then run:
```bash
gradle run
```

## Usage

1. **View Departments**: Click on any department button to see information (navigation stub)
2. **Login**: 
   - Enter email and password
   - Click "Login" button
3. **Sign Up**:
   - Toggle to "Sign Up" mode
   - Enter name, phone, email, and password
   - Click "Sign Up" button

## Components

### Header
- Hospital name and tagline
- Live clock showing current time
- Current date display

### Main Content
- **Departments Section**: Grid of 6 clickable department buttons
- **About Section**: Hospital description
- **Login/Signup Section**: Form with toggle between modes

### Footer
- Contact information with address, phone, and email
- Emergency services information (24/7, emergency numbers)
- Operating hours for different services

## Customization

You can customize the following:

- **Colors**: Modify the `-fx-background-color` styles in the code
- **Departments**: Edit the `departments` array in `createDepartmentsSection()`
- **Hospital Information**: Update text in footer and about sections
- **Form Fields**: Add or remove fields in `createFormFields()`

## Backend Integration

The current implementation shows alert dialogs for form submissions. To integrate with a backend:

1. Replace the `handleSubmit()` method with actual HTTP requests
2. Use libraries like `HttpClient` or `OkHttp` for API calls
3. Implement proper authentication and session management
4. Add error handling and validation

## Notes

- The application currently displays alerts instead of actual backend connections
- Department navigation buttons show information dialogs (implement routing as needed)
- All styles are inline for simplicity (consider using CSS files for larger projects)
- The gradient background is simulated (JavaFX has limited gradient support compared to CSS)

## License
