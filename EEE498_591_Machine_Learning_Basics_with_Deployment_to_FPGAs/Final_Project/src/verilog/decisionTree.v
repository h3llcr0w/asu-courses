`include "params.v";

module decisionTree(	input wire start,
			input real sensor_val [num_features-1:0],
                        input int children_left [num_nodes-1:0],
			input int children_right [num_nodes-1:0],
			input real threshold  [num_nodes-1:0],
                        input reg prediction  [num_nodes-1:0],
			input reg [num_bits_features-1:0] index [num_nodes-1:0],
			output reg potable
		    );

	always@(posedge start) begin
	
		int curr_depth;
	        automatic reg decision=1'b0, done=1'b0;
        	automatic int curr_node='0, prev_node='0;

		for(curr_depth=0;curr_depth<max_tree_depth;curr_depth++) begin
			if(!done) begin
//				$display("Current node: %d", curr_node, index[curr_node]);
				decision = sensor_val[index[curr_node]] <= threshold[curr_node];
				prev_node = curr_node;
//				$display("Sensor Index: %d, Sensor value: %f, Threshold: %f", index[curr_node], sensor_val[index[curr_node]-1], threshold[curr_node]);
				if(decision)
		      	        	curr_node = children_left[prev_node];
				else
					curr_node = children_right[prev_node];
//				$display("Direction: %b, Current: %d, Next: %d", decision, prev_node, curr_node);
				if(curr_node<0) begin
					potable = prediction[prev_node];
					done = 1'b1;
//					$display("Predicted value: %b\n", prediction[prev_node]);
				end
			end
		end
		done = 1'b0;
	end

endmodule
	