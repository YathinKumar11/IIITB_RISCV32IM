    #include "firmware.h" 
    void program4(void)  
    {  
        int marks;   
        marks = 67;   
        
        int grade;
        if(marks > 85 && marks <= 100)  
        {  
            grade=5;
            return;   
        }  
        else if (marks > 60 && marks <= 85)   
        {  
            grade=4;
            return;  
        }  
        else if (marks > 40 && marks <= 60)   
        {  
            grade=3;
            return; 
        }  
        else if (marks > 30 && marks <= 40)   
        {  
            grade=2;
            return;   
        }  
        else   
        {  
            grade=1;
            return;
        }  
    }  
