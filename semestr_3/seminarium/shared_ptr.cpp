template <class T> 
class shared_ptr{
    T* value;
    int ref_count;
    shared_prt(shared_ptr& p){ this.ref_count++ }
    ~shared_ptr(){
        ref_count--;
        if(!ref_count){
            delete this.value;
        }
    }
