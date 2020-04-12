/**
 * Manages the Antarctica election process. 
 *
 * @author Lyndon While
 * @version 1.0 2020
 */
import java.util.ArrayList;

public class Election
{
    // the list of candidates
    private ArrayList<Candidate> candidates;
    // the list of voting papers
    private ArrayList<VotingPaper> papers;
    // the file of election information
    private FileIO file;

    /**
     * Constructor for objects of class Election.
     * Creates the three field objects.
     */
    public Election(String filename)
    {
       // TODO 13
    }
    
    /**
     * Constructor for objects of class Election with default files.
     * It uses k to select from the sample input files.
     */
    public Election(int k)
    {
       this("election" + k + ".txt");
    }
    
    /**
     * Returns the candidates list.
     */
    public ArrayList<Candidate> getCandidates()
    {
       // TODO 14
       return null;
    }
    
    /**
     * Returns the papers list.
     */
    public ArrayList<VotingPaper> getPapers()
    {
       // TODO 15
       return null;
    }
    
    /**
     * Returns the read-in file contents.
     */
    public ArrayList<String> getFile()
    {
       // TODO 16
       return null;
    }
    
    /**
     * Use the file information to initialise the other two fields.
     * Reads the candidates, then discards exactly one blank line, then reads the voting papers.
     * See the sample input files for examples of the format.
     */
    public void processFile() 
    {
       // TODO 17
    }
    
    /**
     * Adds each formal vote to each candidate, both numbers of votes and numbers of wins.
     * Returns the number of informal votes.
     */
    public int conductCount()
    {
       // TODO 21
       return -1;
    }

    /**
     * Returns and prints a summary of the election result. 
     * See the sample output files for the required format. 
     */
    public String getStandings()
    {
       // TODO 22
       return "";
    }
    
    /**
     * Returns the winner of the election. 
     * Selects the candidate with the highest number of votes; if multiple 
     * candidates are equal, selects the one with the highest number of wins. 
    */
    public Candidate winner()
    {
       // TODO 23
       return null;
    }
}