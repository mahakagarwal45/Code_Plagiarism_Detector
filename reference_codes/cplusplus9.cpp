void solve(int row, vector<string>& board, vector<vector<string>>& ans,
    vector<int>& leftRow, vector<int>& upperDiag, vector<int>& lowerDiag, int n) {
if (row == n) {
 ans.push_back(board);
 return;
}
for (int col = 0; col < n; col++) {
 if (leftRow[col] == 0 && lowerDiag[row + col] == 0 && upperDiag[n - 1 + col - row] == 0) {
     board[row][col] = 'Q';
     leftRow[col] = lowerDiag[row + col] = upperDiag[n - 1 + col - row] = 1;
     solve(row + 1, board, ans, leftRow, upperDiag, lowerDiag, n);
     board[row][col] = '.';
     leftRow[col] = lowerDiag[row + col] = upperDiag[n - 1 + col - row] = 0;
 }
}
}
