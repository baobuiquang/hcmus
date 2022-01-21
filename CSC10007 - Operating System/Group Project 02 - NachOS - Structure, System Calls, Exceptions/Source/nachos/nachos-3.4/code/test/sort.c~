#include "syscall.h"
int main()
{
	int i, j;
	int n;
	int arr[100];
	PrintString("\n=============== Chuong trinh sort ===============\n");
	// User input
	PrintString("Xin moi nhap so luong phan tu (n <= 100):\nn = ");
	n = ReadInt();
	for (i = 0; i < n; i++) {
		PrintString("Phan tu thu ");
		PrintInt(i);
		PrintString(": ");
		arr[i] = ReadInt();
	}
	// Bubble Sort
	for (i = 0; i < n-1; i++) {
		for (j = 0; j < n-i-1; j++) {
			if (arr[j] > arr[j+1]) {
				// Swap arr[j] and arr[j+1]
				arr[j] = arr[j] + arr[j+1];
				arr[j+1] = arr[j] - arr[j+1];
				arr[j] = arr[j] - arr[j+1];
			}
		}
	}
	// Print new order
	PrintString("\nSau khi sap xep: ");
	for (i = 0; i < n; i++) {
		if (i != 0) {PrintString(", ");}
		PrintInt(arr[i]);
	}
	PrintString("\n==================================================\n\n");
	return 0;
}
