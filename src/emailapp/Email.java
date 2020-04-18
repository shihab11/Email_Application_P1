package emailapp;

import java.util.Scanner;

public class Email {
    private String firstName;
    private String lastName;
    private String password;
    private String department;
    private String email;
    private int mailboxCapacity = 500;
    private int defaultPasswordLength;
    private String alternativeEmail;
    private String companySuffix = "vgrg.com";

    // Constructor to receive the first name and last name

    public Email(String firstName, String lastName){
        this.firstName = firstName;
        this.lastName = lastName;
        System.out.println("EMAIL CREATED:" + this.firstName + " "+ this.lastName);

        //Call a method asking for department - return the department
        this.department = setDepartment();
        System.out.println("Department:"  + this.department );

        // Call a method that returns a random password
        this.password = randomPassword(8);
        System.out.println("Your password is: "  + this.password);

        //Combine elements to generate email
        email = firstName.toLowerCase() + "." + lastName.toLowerCase() + "@" + department + companySuffix ;
        System.out.println("Your email is: " + email);

    }


    // Ask for the department
    private  String setDepartment() {
        System.out.println("Department CODES \n1 for sales \n2 for Development\n3 for Accounting\n0 for none\nEnter department code: ");
        Scanner in = new Scanner(System.in);
        int depChoice = in.nextInt();
        if (depChoice == 1) { return "sales"; }
        else if (depChoice == 2) { return "dev"; }
        else if (depChoice == 3) { return "acct"; }
        else { return ""; }
    }

    // Generate the random password
    private String randomPassword(int length){
        String passwordSet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%";
        char[] password = new char[length];
        for ( int i = 0; i<length; i++){
            int rand = (int) (Math.random() * passwordSet.length());
            password[i] = passwordSet.charAt(rand);

        }

        return new String(password);
    }


    // Set the mailbox capacity
    public void SetmailboxCapacity(int capacity){
        this.mailboxCapacity = capacity;

    }


    // Set the alternative email
    public void setAlternativeEmail(String alternativeEmail){
      this.alternativeEmail = alternativeEmail;
    }


    // Change the password
    public void changePassword(String password){
        this.password = password;
    }
        public int getMailboxCapacity() { return mailboxCapacity; }
        public String getAlternativeEmail() { return alternativeEmail; }
        public String getPassword() { return password; }

        public String showInfo() {
        return "DISPLAY NAME: " + firstName + " " + lastName +
                "\nCOMPANY EMAIL: " + email +
                "\nMAILBOX CAPACITY: " + mailboxCapacity + " mb";

        }

}
