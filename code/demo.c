#include <stdio.h>
int check(int y[4],int target[4]){
	int i,j;
	for(i=0;i<4;i++){
		if(y[i]!=target[i]){
			return 1;
		}
	}
	return 0;
}
//bipolar activation function
int function(int y_in){
	int theta=0;
	if(y_in<-theta)
		return -1;
	else if(y_in>=-theta && y_in<=theta)
		return 0;
	else if(y_in>theta)
		return 1;
}
void main(){
	int i=0,j,y_in[4]={0,0,0,0},y[4]={0,0,0,0},change_weights[2]={0,0},change_bias=0,new_bias=0,new_weights[2]={0,0},alpha=1;
	// int target[4]={1,-1,-1,-1},x[4][2]={{1,1},{1,-1},{-1,1},{-1,-1}};//and bipolar i/p bipolar o/p
	int target[4]={-1,1,1,1},x[4][2]={{0,0},{0,1},{1,0},{1,1}};//or binary i/p and bipolar o/p
	//epochs
	while(check(y,target)){
		printf("\n-------------------------------------------------------------\nEpoch %d\n-------------------------------------------------------------",i+1);
		printf("\nx1\tx2\ty\tt");
		for(j=0;j<4;j++){
			//calc y_in and y
			y_in[j]=(x[j][0]*new_weights[0]+x[j][1]*new_weights[1])+new_bias;
			y[j]=function(y_in[j]);
			//change weights and bias
			if(y[j]==target[j]){
				change_weights[0]=0;
				change_weights[1]=0;
				change_bias=0;
			}
			else{
				change_weights[0]=alpha*x[j][0]*target[j];
				change_weights[1]=alpha*x[j][1]*target[j];
				change_bias=alpha*target[j];
			}
			//new weights and bias
			new_weights[0]=new_weights[0]+change_weights[0];
			new_weights[1]=new_weights[1]+change_weights[1];
			new_bias=new_bias+change_bias;
			printf("\n%d\t%d\t%d\t%d",x[j][0],x[j][1],y[j],target[j]);
		}
		i++;
	}
	printf("\n");
}
