DEFAULT_CODE_TEMPLATES = {
  'c': r"""
#include <stdio.h>

int main()
{
    printf("hello, world\n");
}
""",
  'cc': r"""
#include<bits/stdc++.h>
#define MAXN 114514
#define INF 1e9
#define MOD 1000000009
#define FILE_NAME "tourist"
#define DEBUG true
using namespace std;

namespace MySolution{
	void in(){
		
	}
	void exec(){
		
	}
	void out(){
		
	}
	void init(){
		in();
		exec();
		out();
	}
}

int main(){
	ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
	if(!DEBUG){
		freopen(FILE_NAME+'.in', "r", stdin);
		freopen(FILE_NAME+'.out', "w", stdout);
	}
	MySolution::init();
	if(!DEBUG) {
		fclose(stdin);
		fclose(stdout);
	}
	return 0;
}
""",
  'pas': r"""
begin
    writeln('hello, world');
end.
""",
  'java': r"""
import java.io.*;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws IOException {
        Scanner sc = new Scanner(System.in);
        System.out.println("hello, world");
    }
}
""",
  'py': r"""

""",
  'py3': r"""

""",
  'php': r"""

""",
  'rs': r"""
fn main() {
  println!("hello, world!");
}
""",
  'hs': r"""
main = putStrLn "hello, world"
""",
}
