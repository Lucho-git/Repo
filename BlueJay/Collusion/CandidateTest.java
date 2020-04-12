import static org.junit.Assert.*;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

/**
 * This class provides unit test cases for the Candidate class.
 * @author Lyndon While
 * @version 1.0
 */
public class CandidateTest
{
    private Candidate c4;
    private double epsilon = 10e-4;

    /**
     * Sets up the test fixture.
     *
     * Called before every test case method.
     */
    @Before
    public void setUp()
    {
        c4 = new Candidate("Dipsy");
    }

    @Test
    public void testCandidate() 
    {
        assertTrue  ("my name is Dipsy",    c4.getName().equals("Dipsy"));
        assertEquals("I have no votes",  0, c4.getNoOfVotes());
        assertEquals("I have no wins", 0.0, c4.getNoOfWins(), epsilon); 
    }

    @Test
    public void testaddToCount() 
    {
        assertEquals("I have 0 votes",   0, c4.getNoOfVotes());
        c4.addToCount(3);
        assertEquals("I have 3 votes",   3, c4.getNoOfVotes());
        c4.addToCount(9);
        assertEquals("I have 12 votes", 12, c4.getNoOfVotes());
    }

    @Test
    public void testaddToWins() 
    {
        assertEquals("I have 0 wins",       0.00, c4.getNoOfWins(), epsilon);
        c4.addToWins(7.0);
        assertEquals("I have 7 wins",       7.00, c4.getNoOfWins(), epsilon);
        c4.addToWins(6.25);
        assertEquals("I have 13.25 votes", 13.25, c4.getNoOfWins(), epsilon);
    }

    @Test
    public void testgetStanding() 
    {
        assertTrue("wrong String returned", c4.getStanding().equals("Dipsy got 0 votes and 0 wins"));
        c4.addToCount(100);
        c4.addToWins(10.5);
        assertTrue("wrong String returned", c4.getStanding().equals("Dipsy got 100 votes and 11 wins"));
        c4.addToCount(212);
        c4.addToWins(16.86);
        assertTrue("wrong String returned", c4.getStanding().equals("Dipsy got 312 votes and 27 wins"));
    }
}
