import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

// Demo users — must match DataSeeder exactly
const DEMO_USERS = [
  { id: 1, name: 'TestUser1', email: 'testuser1@demo.com', city: 'New Delhi',  state: 'Delhi',       country: 'India', latitude: 28.6139, longitude: 77.2090, role: 'USER' },
  { id: 2, name: 'TestUser2', email: 'testuser2@demo.com', city: 'Mumbai',     state: 'Maharashtra', country: 'India', latitude: 19.0760, longitude: 72.8777, role: 'USER' },
  { id: 3, name: 'TestUser3', email: 'testuser3@demo.com', city: 'Bengaluru',  state: 'Karnataka',   country: 'India', latitude: 12.9716, longitude: 77.5946, role: 'USER' },
];

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);

  // Restore previously selected user from localStorage — no backend call needed
  useEffect(() => {
    const savedId = localStorage.getItem('userId');
    if (savedId) {
      const found = DEMO_USERS.find((u) => String(u.id) === savedId);
      if (found) setUser(found);
    }
    setAuthLoading(false);
  }, []);

  const login = (userData) => {
    localStorage.setItem('userId', String(userData.id));
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('userId');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user, authLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
