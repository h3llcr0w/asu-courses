`include "params.v";

module decisionTreee_tb();

	real sensor_val_m [num_features*num_data_rows-1:0];
        reg potable_ref[num_data_rows-1:0];

	real threshold  [num_nodes-1:0];
        reg prediction  [num_nodes-1:0];
        int children_left  [num_nodes-1:0];
        int children_right  [num_nodes-1:0];
	reg [num_bits_features-1:0] index [num_nodes-1:0];

	reg potable, start;
	real sensor_val[num_features-1:0];

	decisionTree DT_dut (.start(start), .sensor_val(sensor_val), .children_left(children_left), .children_right(children_right), .threshold(threshold), .prediction(prediction), .index(index), .potable(potable));

/*      Read sensor values and reference potability values       */
	int p,fp_sen, fp_pot;

	task read_sensor_values();
		fp_sen=$fopen("./sensor_values.txt","r");
		for(int count=0;count<num_features*num_data_rows;count++) begin
		      	p=$fscanf(fp_sen,"%f ",sensor_val_m[count]);
		end
		$fclose(fp_sen);
	endtask

	task read_potability_values();
		fp_pot=$fopen("./potable_ref.txt","r");
		for(int count=0;count<num_data_rows;count++) begin
		      	p=$fscanf(fp_pot,"%b ",potable_ref[count]);
		end
		$fclose(fp_pot);
	endtask

/*       Read pre-trained model information   */

	int fp_th, fp_cl, fp_cr, fp_ind, fp_pred;

	task read_model_threshold();
		fp_sen=$fopen("./model_thresholds.txt","r");
		for(int count=0;count<num_nodes;count++) begin
		      	p=$fscanf(fp_sen,"%f ",threshold[count]);
		end
		$fclose(fp_sen);
	endtask

	task read_model_children_left();
		fp_cl=$fopen("./children_left.txt","r");
		for(int count=0;count<num_nodes;count++) begin
		      	p=$fscanf(fp_cl,"%f ",children_left[count]);
		end
		$fclose(fp_cl);
	endtask

	task read_model_children_right();
		fp_cr=$fopen("./children_right.txt","r");
		for(int count=0;count<num_nodes;count++) begin
		      	p=$fscanf(fp_cr,"%f ",children_right[count]);
		end
		$fclose(fp_cr);
	endtask

	task read_model_sensor_index();
		fp_ind=$fopen("./model_sensor_index.txt","r");
		for(int count=0;count<num_nodes;count++) begin
		      	p=$fscanf(fp_ind,"%f ",index[count]);
		end
		$fclose(fp_ind);
	endtask

	task read_model_prediction();
		fp_pred=$fopen("./model_predictions.txt","r");
		for(int count=0;count<num_nodes;count++) begin
		      	p=$fscanf(fp_pred,"%f ",prediction[count]);
		end
		$fclose(fp_pred);
	endtask


/*  Test functionality   */

	initial begin

		int correct_pred = 0;
		read_sensor_values();
		read_potability_values();

		read_model_threshold();
		read_model_children_left();
		read_model_children_right();
		read_model_sensor_index();
		read_model_prediction();

		for(int i=0;i<num_data_rows;i++) begin
			#2 sensor_val = sensor_val_m[i*num_features+(num_features-1) -: num_features];
			start=1'b1;
			#10 
//                      $display("Expected: %b\tPredicted: %b", potable_ref[i], potable);
			correct_pred += potable_ref[i]==potable;
			start=1'b0;
		end
		$display("Total dataset size: %d", num_data_rows);
		$display("Number of mispredicts: %d", num_data_rows-correct_pred);
		$display("Accuracy: %f", real'(correct_pred)*100/num_data_rows);
		#50 $finish;
	end

endmodule