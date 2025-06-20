class Solution {
    public:
      int majorityElement(vector<int>& arr) {
          // code here
             map <int , int> mp ;
             int size = arr.size();
          for(int i = 0; i<size ; i++){
              mp[arr[i]]++;
          }
          
          for(auto it:mp){
              if(it.second > size/2)
              return it.first;
          }
          
            return -1;
      }
  };