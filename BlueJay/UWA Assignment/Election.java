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
       file = new FileIO(filename);
       candidates = new ArrayList<Candidate>();
       papers = new ArrayList<VotingPaper>();
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
       return candidates;
    }
    
    /**
     * Returns the papers list.
     */
    public ArrayList<VotingPaper> getPapers()
    {
       return papers;
    }
    
    /**
     * Returns the read-in file contents.
     */
    public ArrayList<String> getFile()
    {
       return file.getLines();
    }
    
    /**
     * Use the file information to initialise the other two fields.
     * Reads the candidates, then discards exactly one blank line, then reads the voting papers.
     * See the sample input files for examples of the format.
     */
    //need to initialize, papers and candidates
    public void processFile() 
    {
       ArrayList<String> lines = getFile();
       boolean cont = true;
       int i = 0;
       while(cont)
       {
           String curLine = lines.get(i);
           if(curLine.length()!= 0)
           {
               Candidate candConstr = new Candidate(curLine);
               candidates.add(candConstr);
           }
           else
           {
               cont = false;
           }
           i += 1;
       }
       cont = true;
       for(int x = i; x < lines.size(); x++)
       {
           String curLine = lines.get(x);
           VotingPaper paperConstr = new VotingPaper(curLine);
           papers.add(paperConstr);
       }       
       
    }
    
    /**
     * Adds each formal vote to each candidate, both numbers of votes and numbers of wins.
     * Returns the number of informal votes.
     */
    public int conductCount()
    {
       int informalCount = 0;
       for(VotingPaper paper: papers)
       {
           if(paper.isFormal(candidates.size()))
           {
               paper.updateVoteCounts(candidates);
               paper.updateWinCounts(candidates);
           }
           else
           {
               informalCount ++;
           }
       }
       return informalCount;
    }

    /**
     * Returns and prints a summary of the election result. 
     * See the sample output files for the required format. 
     */
    public String getStandings()
    {
       String standings = "";
       for(Candidate cand: candidates)
       {
           standings += cand.getStanding() + "\n";
       }
       return standings;
    }
    
    /**
     * Returns the winner of the election. 
     * Selects the candidate with the highest number of votes; if multiple 
     * candidates are equal, selects the one with the highest number of wins. 
    */
    public Candidate winner()
    {
       ArrayList<Integer> voteWinners = new ArrayList<Integer>();
       
       //used to hold multiple winning candidate values in the event of same number of votes and of wins
       ArrayList<Integer> voteChampions = new ArrayList<Integer>();

       int voteMax = 0;
       double winMax = 0;
       Candidate winner;
       
       //Find highest number of votes
       for(Candidate cand: candidates)
       {
           if(cand.getNoOfVotes() > voteMax)
           {
               voteMax = cand.getNoOfVotes();
           }
       }
       
       //Group all candidates with highest number of votes together
       for(int i = 0; i < candidates.size(); i++)
       {
           if(candidates.get(i).getNoOfVotes() == voteMax)
           {
               voteWinners.add(i);
           }
       }
       // if there is more than 1 votewinner, decide the winner by number of wins,
       // however there can also be a possible draw with number of votes and with number of wins
       // the instructions do not address this situation, I have added functionality to detect dual winners
       // if it is required for a later date or further instructions,
       if(voteWinners.size() > 1)
       {
           for(int i = 0; i < voteWinners.size(); i++)
           {
               if( candidates.get(  voteWinners.get(i)).getNoOfWins() > winMax)
               {
                  winMax = candidates.get(voteWinners.get(i)).getNoOfWins();
               }
           }
           for(int i = 0; i < voteWinners.size(); i++)
           {
               if(candidates.get( voteWinners.get(i)).getNoOfWins() == winMax)
               {
                   voteChampions.add(voteWinners.get(i));
               }
           }
           winner = candidates.get(voteChampions.get(0));
           if(voteChampions.size() > 1)
           {
               System.out.println("Multiple Winners have been decided, choosing Candidate: " + winner.getName() + " as default winner");
           }
       }
       else
       {
           winner = candidates.get(voteWinners.get(0));
       }   
       System.out.println(getStandings());
       System.out.println("Winner is: " +winner.getName() +"\n");
       return winner;
    }
}