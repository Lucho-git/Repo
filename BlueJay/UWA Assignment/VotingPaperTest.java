import static org.junit.Assert.*;
import org.junit.After;
import org.junit.Before; 
import org.junit.Test;

/**
 * This class provides unit test cases for the VotingPaper class.
 * @author Lyndon While
 * @version 1.0
 */
import java.util.ArrayList;

public class VotingPaperTest
{
    private VotingPaper v4, v4a, v4b, v4c, v4d;
    private ArrayList<Candidate> cs;
    private double epsilon = 10e-4; // precision required from doubles
    
    private String restrue = "result should be true";
    private String resfals = "result should be false";

    /**
     * Sets up the test fixture.
     *
     * Called before every test case method.
     */
    @Before
    public void setUp()
    {
        v4  = new VotingPaper("1,1,0,2");
        v4a = new VotingPaper("1,1,2");    // wrong length, everything else fine
        v4b = new VotingPaper("1,1,4,-2"); // negative number, everything else fine
        v4c = new VotingPaper("1,1,0,3");  // illegal total, everything else fine
        v4d = new VotingPaper("2,2,0,0");
        
        cs = new ArrayList<>();
        cs.add(new Candidate("Dipsy"));
        cs.add(new Candidate("Po"));
        cs.add(new Candidate("Laa Laa"));
        cs.add(new Candidate("Tinky-Winky"));
    }

    @Test
    public void testVotingPaper() 
    {
        assertTrue  ("marks shouldn't be null",     v4.getMarks() != null);
        assertEquals("marks should have size 4", 4, v4.getMarks().size());
        assertEquals("marks is wrong", 1, (int) v4.getMarks().get(0));
        assertEquals("marks is wrong", 1, (int) v4.getMarks().get(1));
        assertEquals("marks is wrong", 0, (int) v4.getMarks().get(2));
        assertEquals("marks is wrong", 2, (int) v4.getMarks().get(3));
    }

    @Test
    public void testisCorrectLength() 
    {
        assertTrue (restrue,  v4.isCorrectLength(4));
        assertFalse(resfals, v4.isCorrectLength(5));
    }

    @Test
    public void testisLegalTotal() 
    {
        assertTrue (restrue, v4.isLegalTotal(4));
        assertTrue (restrue, v4.isLegalTotal(6));
        assertFalse(resfals, v4.isLegalTotal(2));
    }

    @Test
    public void testanyNegativeVotes() 
    {
        assertFalse(resfals,  v4.anyNegativeMarks());
        assertTrue (restrue, v4b.anyNegativeMarks());
    }

    @Test
    public void testisFormal() 
    {
        assertTrue (restrue,  v4.isFormal(4));
        assertFalse(resfals, v4a.isFormal(4)); // wrong length
        assertFalse(resfals, v4b.isFormal(4)); // negative number
        assertFalse(resfals, v4c.isFormal(4)); // illegal total
    }

    @Test
    public void testupdateVoteCounts() 
    {
        v4.updateVoteCounts(cs);
        assertEquals("0 has 1 vote",  1, cs.get(0).getNoOfVotes()); 
        assertEquals("1 has 1 vote",  1, cs.get(1).getNoOfVotes());
        assertEquals("2 has 0 votes", 0, cs.get(2).getNoOfVotes());
        assertEquals("3 has 2 votes", 2, cs.get(3).getNoOfVotes());
        v4d.updateVoteCounts(cs);
        assertEquals("0 has 3 votes", 3, cs.get(0).getNoOfVotes());
        assertEquals("1 has 3 votes", 3, cs.get(1).getNoOfVotes());
        assertEquals("2 has 0 votes", 0, cs.get(2).getNoOfVotes());
        assertEquals("3 has 2 votes", 2, cs.get(3).getNoOfVotes());
        for (Candidate c : cs)
            assertEquals("no one has any wins", 0.0, c.getNoOfWins(), epsilon);
    }

    @Test
    public void testhighestVote() 
    {
        ArrayList<Integer> xs;
        xs = v4.highestVote();
        assertTrue  ("xs shouldn't be null",     xs != null);
        assertEquals("xs should have size 1", 1, xs.size());
        assertTrue  ("xs should contain 3",      xs.contains(3));
        xs = v4d.highestVote();
        assertTrue  ("xs shouldn't be null",     xs != null);
        assertEquals("xs should have size 2", 2, xs.size());
        assertTrue  ("xs should contain 0",      xs.contains(0)); // allows either  
        assertTrue  ("xs should contain 1",      xs.contains(1)); // order on xs
    }

    @Test
    public void testupdateWinCounts() 
    {
        v4.updateWinCounts(cs);
        assertEquals("0 has 0 wins", 0.0, cs.get(0).getNoOfWins(), epsilon);
        assertEquals("1 has 0 wins", 0.0, cs.get(1).getNoOfWins(), epsilon);
        assertEquals("2 has 0 wins", 0.0, cs.get(2).getNoOfWins(), epsilon);
        assertEquals("3 has 1 win",  1.0, cs.get(3).getNoOfWins(), epsilon);
        v4d.updateWinCounts(cs);
        assertEquals("0 has 0.5 wins", 0.5, cs.get(0).getNoOfWins(), epsilon);
        assertEquals("1 has 0.5 wins", 0.5, cs.get(1).getNoOfWins(), epsilon);
        assertEquals("2 has 0 wins",   0.0, cs.get(2).getNoOfWins(), epsilon);
        assertEquals("3 has 1 win",    1.0, cs.get(3).getNoOfWins(), epsilon);
        for (Candidate c : cs)
            assertEquals("no one has any votes", 0, c.getNoOfVotes(), epsilon);
    }
}
