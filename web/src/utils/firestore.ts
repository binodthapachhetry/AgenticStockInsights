import { initializeApp } from 'firebase/app';                                                                                                               
import { getFirestore, collection, query, where, getDocs, connectFirestoreEmulator } from 'firebase/firestore';                                             
import app from '../firebase/config';                                                                                                                       
                                                                                                                                                            
// Connect to the specific database by name                                                                                                                 
const db = getFirestore(app);                                                                                                                               
                                                                                                                                                            
// If you're using a different database than the default one, you need to specify it                                                                        
// This is only available in the Firebase Admin SDK, not in the client SDK                                                                                  
// For client SDK, you would need to use a different project ID that points to that database                                                                
                                                                                                                                                            
export const isEmailApproved = async (email: string): Promise<boolean> => {                                                                                 
  try {                                                                                                                                                     
    console.log("Checking if email is approved:", email);                                                                                                   
                                                                                                                                                            
    // Reference to the approvedUsers collection in your database                                                                                           
    const approvedUsersRef = collection(db, 'approvedClients');                                                                                               
    console.log("Collection reference:", approvedUsersRef);                                                                                                 
                                                                                                                                                            
    const q = query(approvedUsersRef, where('email', '==', email));                                                                                         
    const querySnapshot = await getDocs(q);                                                                                                                 
                                                                                                                                                            
    // Log the results for debugging                                                                                                                        
    console.log("Query snapshot empty?", querySnapshot.empty);                                                                                              
    console.log("Query snapshot size:", querySnapshot.size);                                                                                                
                                                                                                                                                            
    // Log each document found                                                                                                                              
    querySnapshot.forEach(doc => {                                                                                                                          
      console.log("Found document:", doc.id, doc.data());                                                                                                   
    });                                                                                                                                                     
                                                                                                                                                            
    const isApproved = !querySnapshot.empty;                                                                                                                
    console.log("Email approved:", isApproved);                                                                                                             
    return isApproved;                                                                                                                                      
  } catch (error) {                                                                                                                                         
    console.error("Error checking approved email:", error);                                                                                                 
    return false;                                                                                                                                           
  }                                                                                                                                                         
};