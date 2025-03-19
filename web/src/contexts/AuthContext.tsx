import React, { createContext, useContext, useEffect, useState } from 'react';

import { isEmailApproved } from '../utils/firestore';

import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User
} from 'firebase/auth';
import { auth } from '../firebase/config';

interface AuthContextType {
  currentUser: User | null;
  loading: boolean;
  signup: (email: string, password: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setCurrentUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  // const signup = async (email: string, password: string) => {
  //   await createUserWithEmailAndPassword(auth, email, password);
  // };

  const signup = async (email: string, password: string) => {                                                                                                 
    try {                                                                                                                                                     
      // Check if email is in the approved list                                                                                                               
      const approved = await isEmailApproved(email);                                                                                                          
      if (!approved) {       
        console.log('This email is not authorized to create an account')                                                                                                                                  
        throw new Error('This email is not authorized to create an account');   
      }                                                                                                                                                       
      console.log(email, " is authorized to create an account.")                                                                                                                                                       
      // Proceed with signup                                                                                                                                  
      await createUserWithEmailAndPassword(auth, email, password);                                                                                            
    } catch (error: any) {                                                                                                                                    
      console.error("Signup error:", error);                                                                                                                  
      throw error;                                                                                                                                            
    }                                                                                                                                                         
  };


  const login = async (email: string, password: string) => {
    await signInWithEmailAndPassword(auth, email, password);
  };

  const logout = async () => {
    await signOut(auth);
  };

  const value = {
    currentUser,
    loading,
    signup,
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};