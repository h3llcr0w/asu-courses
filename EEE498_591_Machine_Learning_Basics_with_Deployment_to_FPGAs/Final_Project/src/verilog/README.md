## Verilog implementation of Decision Tree Inference Model

* This experiment attempts to create a very basic Decision Tree inference model in hardware, assuming the pre-trained tree information is avaiable in memory.
* Simulations were conducted using Modelsim and found the model to perform as expected, with training accuracy of 100% and test accuracy of 82.87%.

### File Information:
 
decisionTree.v  	// Decision Tree model in SystemVerilog
params.v		// Parameters defining number of features, tree depth and other info 

decisionTree_tb.sv	// Testbench to verify functionality
*.txt			// Supporting files for testbench including tree information and golden outputs generated from Python
