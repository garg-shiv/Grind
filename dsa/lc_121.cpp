class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int ans = 0; 
        int carrier = prices[0]; 

        for(int i = 1; i<prices.size(); i++){
            if(prices[i]>carrier){
                ans = max(ans, prices[i] - carrier);
            }

            carrier = min(carrier, prices[i]); 
        }

        return ans;
    }
};