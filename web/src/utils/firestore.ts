import { getFirestore, collection, query, where, getDocs } from 'firebase/firestore';                                                                       
import app from '../firebase/config';                                                                                                                       
                                                                                                                                                            
const db = getFirestore(app);                                                                                                                               
                                                                                                                                                            
export const isEmailApproved = async (email: string): Promise<boolean> => {                                                                                 
  const approvedUsersRef = collection(db, 'approvedUsers');   
  
  const q = query(approvedUsersRef, where('email', '==', email));                                                                                           
  const querySnapshot = await getDocs(q);                                                                                                                   
  return !querySnapshot.empty;                                                                                                                              
};  