/**
 * Represents a candidate in the Antarctica election process.
 *
 * @author Lyndon While
 * @version 1.0 2020
 */
//TODO MAYBE IMPORT java.lang FOR MATH CLASS 

public class Candidate
{
    // their name
    private String name;
    // their number of votes
    private int noOfVotes;
    // their number of first places 
    private double noOfWins;

    /**
     * Constructor for objects of class Candidate.
     */
    public Candidate(String name)
    {
        //construct imported candidate name
        this.name = name;
        //construct and initialize votes to 0
        this.noOfVotes = 0;
        //construct and initizalizewins to 0
        this.noOfWins = 0;
    }

    /**
     * Returns the candidate's name.
     */
    public String getName()
    {
       return name;
    }

    /**
     * Returns the number of votes obtained by the candidate.
     */
    public int getNoOfVotes()
    {
        return noOfVotes;
    }

    /**
     * Returns the number of wins obtained by the candidate.
     */
    public double getNoOfWins()
    {
       return noOfWins;
    }
    
    /**
     * Adds n votes to the candidate. 
     */
    public void addToCount(int n)
    {
       //adds number of votes to votecount
       noOfVotes += n;
    }
    
    /**
     * Adds n wins to the candidate. 
     */
    public void addToWins(double n)
    {
       // adds number of wins to wincount, wincount is a real number
       noOfWins += n;
    }

    /**
     * Returns a string reporting the candidate's result, 
     * rounding the number of wins to the nearest integer. 
     * See the sample output files for the required format. 
     */
    public String getStanding()
    {
       // Create an output string containing a candidate summary
       // TODO round up or down noOfWins to an int
       return name + " got " + noOfVotes + " votes and " + Math.round(noOfWins) +" wins\n";
    }
}
