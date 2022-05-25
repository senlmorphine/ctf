#include <iostream>
#include <cstring>
#include "obfuscate.h"

int main(int argc, char **argv) {
  std::cout << "The flag is " 
            << strlen(AY_OBFUSCATE("MCSC{i_need_your_opinion_in_whats_the_best_dynamic_or_static}"))
            << " too much long."
            << std::endl;
}
