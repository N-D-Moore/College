package sudokuSolver;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
//import java.awt.TextArea;

public class SwingSudokuSolver extends sudokuSolver{
	private JFrame mainFrame;
	private JLabel solveLabel;
	private JPanel controlPanel;
	//private JTextArea BoardTextArea;
	
	public SwingSudokuSolver(){
		mainFrame = new JFrame("Sudoku Solver Program.");
		mainFrame.setSize(500, 500);
		mainFrame.setLayout(new GridLayout(2, 1));
		
		solveLabel = new JLabel("Choose your puzzle.",JLabel.CENTER );
		//BoardTextArea = new JTextArea("");
		
		mainFrame.addWindowListener(new WindowAdapter() {
	         public void windowClosing(WindowEvent windowEvent){
	            System.exit(0);
	         }    
		});
		
		controlPanel = new JPanel();
	    controlPanel.setLayout(new FlowLayout());
	    
	    
	    mainFrame.add(solveLabel);
	    mainFrame.add(controlPanel);
	   // mainFrame.add(BoardTextArea);
	    
	    
	    mainFrame.setVisible(true);
	}
	
	public void ShowOptions()
	{
		
		
		JButton sample1 = new JButton("Sample #1");
		JButton sample2 = new JButton("Sample #2");
		JButton sample3 = new JButton("Sample #3");
		JButton sample4 = new JButton("Sample #4");
		
		sample1.setActionCommand("Sample #1");
		sample2.setActionCommand("Sample #2");
		sample3.setActionCommand("Sample #3");
		sample4.setActionCommand("Sample #4");
		
		sample1.addActionListener(new ButtonListener());
		sample2.addActionListener(new ButtonListener());
		sample3.addActionListener(new ButtonListener());
		sample4.addActionListener(new ButtonListener());
		
		controlPanel.add(sample1);
		controlPanel.add(sample2);
		controlPanel.add(sample3);
		controlPanel.add(sample4);
		
		mainFrame.setVisible(true);
	}
	
	private class ButtonListener implements ActionListener
	{	
		@Override
		public void actionPerformed(ActionEvent e) {
			// TODO Auto-generated method stub
			String command = e.getActionCommand();
			
			if (command.equals("Sample #1")){
				int[][] matrix = parseProblem("samplesudoku1.txt");
				writeMatrix(matrix);
				if (solve(0,0,matrix)) 
					writeMatrix(matrix);
				else
					System.out.println("NONE");
			} else if (command.equals("Sample #2")){
				int[][] matrix = parseProblem("samplesudoku2.txt");
				writeMatrix(matrix);
				if (solve(0,0,matrix)) 
					writeMatrix(matrix);
				else
					System.out.println("NONE");
			} else if (command.equals("Sample #3")){
				int[][] matrix = parseProblem("samplesudoku3.txt");
				writeMatrix(matrix);
				if (solve(0,0,matrix)) 
					writeMatrix(matrix);
				else
					System.out.println("NONE");
			} else {
				int[][] matrix = parseProblem("samplesudoku4.txt");
				writeMatrix(matrix);
				if (solve(0,0,matrix)) 
					writeMatrix(matrix);
				else
					System.out.println("NONE");
			}
			
			
		}
		
	}
	
}
