import java.util.Scanner;
import java.io.FileInputStream;
import java.io.FileNotFoundException;

public class sudokuSolver {
	public static void main(String[] args) {
        int[][] matrix = parseProblem("samplesudoku5.txt");
        writeMatrix(matrix);
        if (solve(0,0,matrix))    // solves in place
            writeMatrix(matrix);
        else
            System.out.println("NONE");
    }

    static boolean solve(int i, int j, int[][] cells) {
        if (i == 9) {
            i = 0;
            if (++j == 9)
                return true;
        }
        if (cells[i][j] != 0)  // skip filled cells
            return solve(i+1,j,cells);

        for (int val = 1; val <= 9; ++val) {
            if (legal(i,j,val,cells)) {
                cells[i][j] = val;
                if (solve(i+1,j,cells))
                    return true;
            }
        }
        cells[i][j] = 0; // reset on backtrack
        return false;
    }

    static boolean legal(int i, int j, int val, int[][] cells) {
        for (int k = 0; k < 9; ++k)  // row
            if (val == cells[k][j])
                return false;

        for (int k = 0; k < 9; ++k) // col
            if (val == cells[i][k])
                return false;

        int boxRowOffset = (i / 3)*3;
        int boxColOffset = (j / 3)*3;
        for (int k = 0; k < 3; ++k) // box
            for (int m = 0; m < 3; ++m)
                if (val == cells[boxRowOffset+k][boxColOffset+m])
                    return false;

        return true; // no violations, so it's legal
    }
    static void writeMatrix(int[][] solution) {
        for (int i = 0; i < 9; ++i) {
            if (i % 3 == 0)
                System.out.println(" -----------------------");
            for (int j = 0; j < 9; ++j) {
                if (j % 3 == 0) System.out.print("| ");
                System.out.print(solution[i][j] == 0
                                 ? " "
                                 : Integer.toString(solution[i][j]));

                System.out.print(' ');
            }
            System.out.println("|");
        }
        System.out.println(" -----------------------");
    }

    static int[][] parseProblem(String fileName) {
		Scanner sudokuFileIn = null;
		int[] puzzle = new int[81];
		int[][] problem = new int[9][9];
		int i = 0;
		int j;
		
		try{
			sudokuFileIn = new Scanner(new FileInputStream(fileName));	
		}
		catch (FileNotFoundException e){
			System.out.println("File not found.");
			System.exit(0);
		}
		
		while (sudokuFileIn.hasNextInt()){
			puzzle[i++] = sudokuFileIn.nextInt();
		}
		for (j=0; j<81; j++){
			//System.out.print(puzzle[j]);
			problem[j/9][j%9] = puzzle[j];		
		}
/*		System.out.println();
		for(i=0;i<9;i++){
			for(j=0;j<9;j++){
				System.out.print(problem[i][j]);
			}
			System.out.println();
		}
*/		sudokuFileIn.close();
		return problem;
	}
	
}
