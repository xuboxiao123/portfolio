#include <iostream>
#include <vector>
int main(){std::vector<int> readings{21,24,29};for(int x:readings)std::cout<<x<<" ";std::cout<<"\ncount="<<readings.size()<<"\n";}