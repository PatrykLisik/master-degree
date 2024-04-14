
template <class T> 
class unique_ptr{
    T* value;
    unique_ptr(unique_ptr& p) = delete; //copy contructor
    unique_ptr& operator=(unique_ptr& p)= delete; //copy assigment
}
