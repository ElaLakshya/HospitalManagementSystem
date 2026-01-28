import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;
import javafx.animation.Timeline;
import javafx.animation.KeyFrame;
import javafx.util.Duration;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class HospitalHomepage extends Application {
    
    private Label timeLabel;
    private Label dateLabel;
    private boolean isLoginMode = true;
    private TextField emailField;
    private PasswordField passwordField;
    private TextField nameField;
    private TextField phoneField;
    private VBox formContainer;
    
    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("MediCare Hospital");
        
        // Main container
        BorderPane root = new BorderPane();
        root.setStyle("-fx-background-color: linear-gradient(to bottom right, #eff6ff, #ecfeff);");
        
        // Header
        root.setTop(createHeader());
        
        // Main content
        root.setCenter(createMainContent());
        
        // Footer
        root.setBottom(createFooter());
        
        // Start clock
        startClock();
        
        Scene scene = new Scene(root, 1200, 900);
        primaryStage.setScene(scene);
        primaryStage.show();
    }
    
    private VBox createHeader() {
        VBox header = new VBox();
        header.setStyle("-fx-background-color: white; -fx-effect: dropshadow(gaussian, rgba(0,0,0,0.1), 10, 0, 0, 2);");
        header.setPadding(new Insets(20, 40, 20, 40));
        
        HBox headerContent = new HBox();
        headerContent.setAlignment(Pos.CENTER);
        headerContent.setSpacing(20);
        
        // Left side - Title
        VBox titleBox = new VBox(5);
        Label titleLabel = new Label("MediCare Hospital");
        titleLabel.setFont(Font.font("System", FontWeight.BOLD, 36));
        titleLabel.setTextFill(Color.rgb(30, 58, 138));
        
        Label subtitleLabel = new Label("Committed to Your Health & Wellness");
        subtitleLabel.setFont(Font.font("System", 14));
        subtitleLabel.setTextFill(Color.rgb(75, 85, 99));
        
        titleBox.getChildren().addAll(titleLabel, subtitleLabel);
        
        // Spacer
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        
        // Right side - Date and Time
        VBox dateTimeBox = new VBox(5);
        dateTimeBox.setAlignment(Pos.CENTER_RIGHT);
        
        timeLabel = new Label();
        timeLabel.setFont(Font.font("System", FontWeight.SEMI_BOLD, 18));
        timeLabel.setTextFill(Color.rgb(30, 64, 175));
        
        dateLabel = new Label();
        dateLabel.setFont(Font.font("System", 12));
        dateLabel.setTextFill(Color.rgb(75, 85, 99));
        
        dateTimeBox.getChildren().addAll(timeLabel, dateLabel);
        
        headerContent.getChildren().addAll(titleBox, spacer, dateTimeBox);
        header.getChildren().add(headerContent);
        
        return header;
    }
    
    private ScrollPane createMainContent() {
        HBox mainContent = new HBox(20);
        mainContent.setPadding(new Insets(30, 40, 30, 40));
        mainContent.setAlignment(Pos.TOP_CENTER);
        
        // Left side - Departments and About
        VBox leftSide = new VBox(20);
        HBox.setHgrow(leftSide, Priority.ALWAYS);
        leftSide.setMaxWidth(Double.MAX_VALUE);
        
        leftSide.getChildren().addAll(createDepartmentsSection(), createAboutSection());
        
        // Right side - Login/Signup
        VBox rightSide = createLoginSignupSection();
        rightSide.setPrefWidth(350);
        
        mainContent.getChildren().addAll(leftSide, rightSide);
        
        ScrollPane scrollPane = new ScrollPane(mainContent);
        scrollPane.setFitToWidth(true);
        scrollPane.setStyle("-fx-background: transparent; -fx-background-color: transparent;");
        
        return scrollPane;
    }
    
    private VBox createDepartmentsSection() {
        VBox section = new VBox(15);
        section.setStyle("-fx-background-color: white; -fx-background-radius: 10; -fx-effect: dropshadow(gaussian, rgba(0,0,0,0.1), 10, 0, 0, 2);");
        section.setPadding(new Insets(25));
        
        Label title = new Label("Our Departments");
        title.setFont(Font.font("System", FontWeight.BOLD, 24));
        title.setTextFill(Color.rgb(30, 58, 138));
        
        GridPane grid = new GridPane();
        grid.setHgap(15);
        grid.setVgap(15);
        
        String[] departments = {"Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Emergency", "Radiology"};
        
        for (int i = 0; i < departments.length; i++) {
            Button deptButton = createDepartmentButton(departments[i]);
            grid.add(deptButton, i % 2, i / 2);
        }
        
        section.getChildren().addAll(title, grid);
        return section;
    }
    
    private Button createDepartmentButton(String departmentName) {
        Button button = new Button(departmentName);
        button.setPrefWidth(250);
        button.setPrefHeight(80);
        button.setStyle(
            "-fx-background-color: linear-gradient(to right, #3b82f6, #06b6d4);" +
            "-fx-text-fill: white;" +
            "-fx-font-size: 16px;" +
            "-fx-font-weight: bold;" +
            "-fx-background-radius: 8;" +
            "-fx-cursor: hand;"
        );
        
        button.setOnMouseEntered(e -> {
            button.setStyle(
                "-fx-background-color: linear-gradient(to right, #2563eb, #0891b2);" +
                "-fx-text-fill: white;" +
                "-fx-font-size: 16px;" +
                "-fx-font-weight: bold;" +
                "-fx-background-radius: 8;" +
                "-fx-cursor: hand;" +
                "-fx-scale-x: 1.05;" +
                "-fx-scale-y: 1.05;"
            );
        });
        
        button.setOnMouseExited(e -> {
            button.setStyle(
                "-fx-background-color: linear-gradient(to right, #3b82f6, #06b6d4);" +
                "-fx-text-fill: white;" +
                "-fx-font-size: 16px;" +
                "-fx-font-weight: bold;" +
                "-fx-background-radius: 8;" +
                "-fx-cursor: hand;"
            );
        });
        
        button.setOnAction(e -> {
            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setTitle(departmentName);
            alert.setHeaderText("Department: " + departmentName);
            alert.setContentText("You clicked on " + departmentName + " department.\n(Navigation would be implemented here)");
            alert.showAndWait();
        });
        
        return button;
    }
    
    private VBox createAboutSection() {
        VBox section = new VBox(15);
        section.setStyle("-fx-background-color: white; -fx-background-radius: 10; -fx-effect: dropshadow(gaussian, rgba(0,0,0,0.1), 10, 0, 0, 2);");
        section.setPadding(new Insets(25));
        
        Label title = new Label("About Us");
        title.setFont(Font.font("System", FontWeight.BOLD, 24));
        title.setTextFill(Color.rgb(30, 58, 138));
        
        Label description = new Label(
            "MediCare Hospital is a leading healthcare institution dedicated to providing " +
            "exceptional medical services with state-of-the-art facilities and experienced " +
            "medical professionals. We offer comprehensive healthcare solutions across " +
            "multiple specialties, ensuring the highest standards of patient care and safety."
        );
        description.setWrapText(true);
        description.setFont(Font.font("System", 14));
        description.setTextFill(Color.rgb(55, 65, 81));
        description.setLineSpacing(3);
        
        section.getChildren().addAll(title, description);
        return section;
    }
    
    private VBox createLoginSignupSection() {
        VBox section = new VBox(20);
        section.setStyle("-fx-background-color: white; -fx-background-radius: 10; -fx-effect: dropshadow(gaussian, rgba(0,0,0,0.1), 10, 0, 0, 2);");
        section.setPadding(new Insets(25));
        
        // Toggle buttons
        HBox toggleBox = new HBox();
        toggleBox.setStyle("-fx-background-color: #f3f4f6; -fx-background-radius: 8;");
        toggleBox.setPadding(new Insets(5));
        toggleBox.setSpacing(0);
        
        Button loginButton = new Button("Login");
        Button signupButton = new Button("Sign Up");
        
        loginButton.setPrefWidth(150);
        signupButton.setPrefWidth(150);
        
        loginButton.setPrefHeight(40);
        signupButton.setPrefHeight(40);
        
        updateToggleButton(loginButton, true);
        updateToggleButton(signupButton, false);
        
        loginButton.setOnAction(e -> {
            isLoginMode = true;
            updateToggleButton(loginButton, true);
            updateToggleButton(signupButton, false);
            updateForm();
        });
        
        signupButton.setOnAction(e -> {
            isLoginMode = false;
            updateToggleButton(loginButton, false);
            updateToggleButton(signupButton, true);
            updateForm();
        });
        
        toggleBox.getChildren().addAll(loginButton, signupButton);
        
        // Form container
        formContainer = new VBox(15);
        createFormFields();
        
        section.getChildren().addAll(toggleBox, formContainer);
        return section;
    }
    
    private void updateToggleButton(Button button, boolean active) {
        if (active) {
            button.setStyle(
                "-fx-background-color: #2563eb;" +
                "-fx-text-fill: white;" +
                "-fx-background-radius: 6;" +
                "-fx-font-size: 14px;" +
                "-fx-cursor: hand;"
            );
        } else {
            button.setStyle(
                "-fx-background-color: transparent;" +
                "-fx-text-fill: #6b7280;" +
                "-fx-background-radius: 6;" +
                "-fx-font-size: 14px;" +
                "-fx-cursor: hand;"
            );
        }
    }
    
    private void createFormFields() {
        formContainer.getChildren().clear();
        
        if (!isLoginMode) {
            // Name field
            VBox nameBox = createFormField("Full Name", "John Doe");
            nameField = (TextField) ((HBox) nameBox.getChildren().get(1)).getChildren().get(0);
            formContainer.getChildren().add(nameBox);
            
            // Phone field
            VBox phoneBox = createFormField("Phone Number", "+1 234 567 8900");
            phoneField = (TextField) ((HBox) phoneBox.getChildren().get(1)).getChildren().get(0);
            formContainer.getChildren().add(phoneBox);
        }
        
        // Email field
        VBox emailBox = createFormField("Email", "your@email.com");
        emailField = (TextField) ((HBox) emailBox.getChildren().get(1)).getChildren().get(0);
        formContainer.getChildren().add(emailBox);
        
        // Password field
        VBox passwordBox = new VBox(5);
        Label passwordLabel = new Label("Password");
        passwordLabel.setFont(Font.font("System", FontWeight.MEDIUM, 12));
        passwordLabel.setTextFill(Color.rgb(55, 65, 81));
        
        HBox passwordInputBox = new HBox();
        passwordField = new PasswordField();
        passwordField.setPromptText("••••••••");
        passwordField.setPrefHeight(40);
        passwordField.setStyle(
            "-fx-background-color: white;" +
            "-fx-border-color: #d1d5db;" +
            "-fx-border-radius: 6;" +
            "-fx-background-radius: 6;" +
            "-fx-padding: 0 10;"
        );
        HBox.setHgrow(passwordField, Priority.ALWAYS);
        
        passwordInputBox.getChildren().add(passwordField);
        passwordBox.getChildren().addAll(passwordLabel, passwordInputBox);
        formContainer.getChildren().add(passwordBox);
        
        // Submit button
        Button submitButton = new Button(isLoginMode ? "Login" : "Sign Up");
        submitButton.setPrefHeight(40);
        submitButton.setMaxWidth(Double.MAX_VALUE);
        submitButton.setStyle(
            "-fx-background-color: #2563eb;" +
            "-fx-text-fill: white;" +
            "-fx-font-size: 14px;" +
            "-fx-font-weight: bold;" +
            "-fx-background-radius: 6;" +
            "-fx-cursor: hand;"
        );
        
        submitButton.setOnMouseEntered(e -> {
            submitButton.setStyle(
                "-fx-background-color: #1d4ed8;" +
                "-fx-text-fill: white;" +
                "-fx-font-size: 14px;" +
                "-fx-font-weight: bold;" +
                "-fx-background-radius: 6;" +
                "-fx-cursor: hand;"
            );
        });
        
        submitButton.setOnMouseExited(e -> {
            submitButton.setStyle(
                "-fx-background-color: #2563eb;" +
                "-fx-text-fill: white;" +
                "-fx-font-size: 14px;" +
                "-fx-font-weight: bold;" +
                "-fx-background-radius: 6;" +
                "-fx-cursor: hand;"
            );
        });
        
        submitButton.setOnAction(e -> handleSubmit());
        
        formContainer.getChildren().add(submitButton);
        
        // Forgot password link (only for login)
        if (isLoginMode) {
            Hyperlink forgotLink = new Hyperlink("Forgot Password?");
            forgotLink.setFont(Font.font("System", 12));
            forgotLink.setStyle("-fx-text-fill: #2563eb;");
            HBox linkBox = new HBox(forgotLink);
            linkBox.setAlignment(Pos.CENTER);
            formContainer.getChildren().add(linkBox);
        }
    }
    
    private VBox createFormField(String labelText, String placeholder) {
        VBox fieldBox = new VBox(5);
        
        Label label = new Label(labelText);
        label.setFont(Font.font("System", FontWeight.MEDIUM, 12));
        label.setTextFill(Color.rgb(55, 65, 81));
        
        HBox inputBox = new HBox();
        TextField textField = new TextField();
        textField.setPromptText(placeholder);
        textField.setPrefHeight(40);
        textField.setStyle(
            "-fx-background-color: white;" +
            "-fx-border-color: #d1d5db;" +
            "-fx-border-radius: 6;" +
            "-fx-background-radius: 6;" +
            "-fx-padding: 0 10;"
        );
        HBox.setHgrow(textField, Priority.ALWAYS);
        
        inputBox.getChildren().add(textField);
        fieldBox.getChildren().addAll(label, inputBox);
        
        return fieldBox;
    }
    
    private void updateForm() {
        createFormFields();
    }
    
    private void handleSubmit() {
        if (isLoginMode) {
            String email = emailField.getText();
            String password = passwordField.getText();
            
            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setTitle("Login");
            alert.setHeaderText("Login Attempt");
            alert.setContentText("Login attempt for: " + email + "\n(Backend connection would be implemented here)");
            alert.showAndWait();
        } else {
            String name = nameField.getText();
            String phone = phoneField.getText();
            String email = emailField.getText();
            
            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setTitle("Sign Up");
            alert.setHeaderText("Sign Up Request");
            alert.setContentText("Signup request for: " + name + "\n(Backend connection would be implemented here)");
            alert.showAndWait();
        }
    }
    
    private VBox createFooter() {
        VBox footer = new VBox(20);
        footer.setStyle("-fx-background-color: #111827;");
        footer.setPadding(new Insets(30, 40, 30, 40));
        
        HBox footerContent = new HBox(40);
        footerContent.setAlignment(Pos.TOP_LEFT);
        
        // Contact Information
        VBox contactBox = new VBox(10);
        Label contactTitle = new Label("Contact Information");
        contactTitle.setFont(Font.font("System", FontWeight.BOLD, 18));
        contactTitle.setTextFill(Color.WHITE);
        
        Label address = new Label("📍 123 Healthcare Avenue, Medical District\n   New York, NY 10001");
        Label phone = new Label("📞 +1 (555) 123-4567");
        Label email = new Label("✉ info@medicarehospital.com");
        
        address.setTextFill(Color.WHITE);
        phone.setTextFill(Color.WHITE);
        email.setTextFill(Color.WHITE);
        
        contactBox.getChildren().addAll(contactTitle, address, phone, email);
        
        // Emergency Services
        VBox emergencyBox = new VBox(10);
        Label emergencyTitle = new Label("Emergency Services");
        emergencyTitle.setFont(Font.font("System", FontWeight.BOLD, 18));
        emergencyTitle.setTextFill(Color.WHITE);
        
        Label emergency247 = new Label("24/7 Emergency Care Available");
        Label emergency911 = new Label("Emergency: 911");
        emergency911.setFont(Font.font("System", FontWeight.BOLD, 16));
        emergency911.setTextFill(Color.rgb(248, 113, 113));
        
        Label ambulance = new Label("Ambulance: +1 (555) 999-0000");
        ambulance.setFont(Font.font("System", FontWeight.SEMI_BOLD, 14));
        ambulance.setTextFill(Color.rgb(250, 204, 21));
        
        emergency247.setTextFill(Color.WHITE);
        
        emergencyBox.getChildren().addAll(emergencyTitle, emergency247, emergency911, ambulance);
        
        // Operating Hours
        VBox hoursBox = new VBox(10);
        Label hoursTitle = new Label("Operating Hours");
        hoursTitle.setFont(Font.font("System", FontWeight.BOLD, 18));
        hoursTitle.setTextFill(Color.WHITE);
        
        Label opd = new Label("OPD: Mon-Sat, 8:00 AM - 8:00 PM");
        Label emergency = new Label("Emergency: 24/7");
        Label lab = new Label("Lab Services: Mon-Sun, 7:00 AM - 9:00 PM");
        
        opd.setTextFill(Color.WHITE);
        emergency.setTextFill(Color.WHITE);
        lab.setTextFill(Color.WHITE);
        
        hoursBox.getChildren().addAll(hoursTitle, opd, emergency, lab);
        
        footerContent.getChildren().addAll(contactBox, emergencyBox, hoursBox);
        
        // Copyright
        VBox copyrightBox = new VBox(5);
        copyrightBox.setAlignment(Pos.CENTER);
        copyrightBox.setStyle("-fx-border-color: #374151; -fx-border-width: 1 0 0 0;");
        copyrightBox.setPadding(new Insets(20, 0, 0, 0));
        
        Label copyright = new Label("© 2025 MediCare Hospital. All rights reserved.");
        copyright.setTextFill(Color.WHITE);
        copyright.setFont(Font.font("System", 12));
        
        Label accreditation = new Label("Accredited by Joint Commission | ISO 9001:2015 Certified");
        accreditation.setTextFill(Color.rgb(156, 163, 175));
        accreditation.setFont(Font.font("System", 11));
        
        copyrightBox.getChildren().addAll(copyright, accreditation);
        
        footer.getChildren().addAll(footerContent, copyrightBox);
        return footer;
    }
    
    private void startClock() {
        Timeline clock = new Timeline(new KeyFrame(Duration.ZERO, e -> {
            LocalDateTime now = LocalDateTime.now();
            DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("hh:mm:ss a");
            DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("EEEE, MMMM dd, yyyy");
            
            timeLabel.setText("🕐 " + now.format(timeFormatter));
            dateLabel.setText("📅 " + now.format(dateFormatter));
        }),
        new KeyFrame(Duration.seconds(1))
        );
        clock.setCycleCount(Timeline.INDEFINITE);
        clock.play();
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}
