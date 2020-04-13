/**
 * Represents a voting paper in the Antarctica election process. 
 *
 * @author Lyndon While
 * @version 1.0 2020
 */
import java.util.ArrayList;
 
public class VotingPaper
{
    // the numbers marked on the paper 
    private ArrayList<Integer> marks;

    /**
     * Constructor for objects of class VotingPaper. 
     * s will be a (possibly empty) sequence of integers, separated by commas. 
     * e.g. if s is "1,22,-13,456", marks is set to <1,22,-13,456>. 
     */
    public VotingPaper(String s)
    {
       marks = new ArrayList<>();
       if (!s.isEmpty())
          for (String x : s.split(",")) 
              marks.add(Integer.parseInt(x));
    }
    
    /**
     * Returns the contents of the paper.
     */
    public ArrayList<Integer> getMarks()
    {
       // returns marks in an array list
       return marks;
    }

    /**
     * Returns true iff the paper has the correct number of marks, 
     * i.e. one for each candidate. 
     */
    public boolean isCorrectLength(int noOfCandidates)
    {
       // TODO CHECK marks.length() is correct
       boolean valid = true;
       if (marks.size() != noOfCandidates)
       {
          valid = false;
       }
       return valid;
    }

    /**
     * Returns true iff the sum of the marks is legal, 
     * i.e. no more than total. 
     */
    public boolean isLegalTotal(int total)
    {
       //set total to 0 and valid to true
       int temp_total = 0;
       boolean valid = true;
       for (int temp : marks)
       {
          temp_total += temp;
       }
       if( temp_total > total)
       {
           valid = false;
       }
       return valid;
    }

    /**
     * Returns true iff there are negative marks. 
     */
    public boolean anyNegativeMarks()
    {
       //valid is always true unless a negative mark is found in which case it is always false
       boolean valid = false;
       for (int temp : marks)
       {

          if(temp < 0)
          {
              valid = true;
          }
       }
       return valid;
    }

    /**
     * Returns true iff the paper is formal. 
     * It must be the right length with no negative marks and a legal total. 
     */
    public boolean isFormal(int noOfCandidates)
    {
       //calls 3 previous functions checking for right length, no negative marks 
       //and a legal total, if any of these are false the voting paper is invalid
       boolean valid = true;
       if(!isCorrectLength(noOfCandidates))
       {
           valid = false;
       }
       if(!isLegalTotal(noOfCandidates))
       {
           valid = false;
       }
       if(anyNegativeMarks())
       {
           valid = false;
       }
       return valid;
    }
    
    /**
     * Adds the appropriate number of votes to each candidate.
     * The kth number goes to the kth candidate.
     */
    public void updateVoteCounts(ArrayList<Candidate> cs)
    {
          for(int i = 0; i < cs.size(); i++)
          {
             cs.get(i).addToCount(marks.get(i));
          }

    }

    /**
     * Returns the indices in marks which have the highest number.
     * e.g. if marks = <4,4,1,5,2>, it returns <3> (because the highest number is at index 3).
     * e.g. if marks = <5,4,1,2,5>, it returns <0,4>.
     * e.g. if marks = <1,1,1,1,1>, it returns <0,1,2,3,4>.
     */
    public ArrayList<Integer> highestVote()
    {
       ArrayList<Integer> highestvotes = new ArrayList<Integer>();
       int max = 0;
       for(int temp:marks)
       {
           if(temp > max)
           {
               max = temp;
           }
       }
       for(int i = 0; i < marks.size(); i++)
       {
           if(marks.get(i) == max)
           {
               highestvotes.add(i);
           }
       }
       return highestvotes;
    }
    
    /**
     * Adds the appropriate number of wins to each candidate.
     * If there are n equal-highest numbers, each of those 
     * candidates receives 1/n wins. 
     */
    public void updateWinCounts(ArrayList<Candidate> cs)
    {

          //retrieves the wincounts using highestvotes()
          ArrayList<Integer>highestVotes = highestVote();
          //assign 1/n win value if there are multiple winners
          double voteValue = 1/(double)highestVotes.size();
          for(int i = 0; i < highestVotes.size(); i++)
          {
              cs.get(highestVotes.get(i)).addToWins(voteValue);
          }
    }
}
