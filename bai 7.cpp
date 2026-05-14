// bai 7.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>

using namespace std;


int main()
{
	int chisocu, chisomoi, sodien , tien = 0;
	cout << " nhap chi so cu : ";
	cin >> chisocu;
	cout << " nhap chi so moi : ";
	cin >> chisomoi;
	if (chisocu < chisomoi) {
		cout << " chi so moi phai lon hon chi so cu /n";
		return 0;
	}
	int sodien = chisomoi - chisocu;
	if (sodien <= 100)
		tien = sodien * 1000;
	else if (sodien <= 150)
		tien = 50 * 1000 + (sodien * 1200);
	cout << " so dien su dung " << sodien << endl;
	cout << "so tien can tra " << tien << endl;

}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
