import React, { useState } from 'react';
import {
  Box, Paper, Typography, Button, Avatar, Divider,
} from '@mui/material';
import { AccountCircle, LocationOn } from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// ── Demo users — hardcoded, no backend needed ─────────────
const DEMO_USERS = [
  { id: 1, name: 'TestUser1', email: 'testuser1@demo.com', city: 'New Delhi',  state: 'Delhi',       country: 'India', latitude: 28.6139, longitude: 77.2090, role: 'USER' },
  { id: 2, name: 'TestUser2', email: 'testuser2@demo.com', city: 'Mumbai',     state: 'Maharashtra', country: 'India', latitude: 19.0760, longitude: 72.8777, role: 'USER' },
  { id: 3, name: 'TestUser3', email: 'testuser3@demo.com', city: 'Bengaluru',  state: 'Karnataka',   country: 'India', latitude: 12.9716, longitude: 77.5946, role: 'USER' },
];

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const from = location.state?.from?.pathname || '/';
  const [selecting, setSelecting] = useState(null);

  const handleSelect = (user) => {
    setSelecting(user.id);
    login(user);
    navigate(from, { replace: true });
  };

  return (
    <Box sx={{
      minHeight: '80vh', display: 'flex', alignItems: 'center',
      justifyContent: 'center', bgcolor: '#f5f5f5', px: 2,
    }}>
      <Box sx={{ width: '100%', maxWidth: 420 }}>

        {/* Logo */}
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <Typography sx={{
            fontWeight: 900, fontSize: '2rem', color: '#131921',
            fontFamily: 'Georgia, serif',
          }}>
            amazon
          </Typography>
        </Box>

        <Paper variant="outlined" sx={{ p: 3, borderRadius: 2 }}>
          <Typography variant="h5" sx={{ fontWeight: 700, mb: 0.5 }}>Sign in</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Choose a demo account to continue
          </Typography>

          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
            {DEMO_USERS.map((u) => (
              <Button
                key={u.id}
                fullWidth
                variant="outlined"
                disabled={selecting === u.id}
                onClick={() => handleSelect(u)}
                sx={{
                  textTransform: 'none',
                  borderRadius: '12px',
                  borderColor: '#ddd',
                  p: 1.5,
                  justifyContent: 'flex-start',
                  gap: 1.5,
                  '&:hover': { borderColor: '#FF9900', bgcolor: '#fff8f0' },
                }}
              >
                <Avatar sx={{ bgcolor: '#FF9900', color: '#131921', width: 40, height: 40, flexShrink: 0 }}>
                  <AccountCircle />
                </Avatar>
                <Box sx={{ textAlign: 'left', flex: 1 }}>
                  <Typography sx={{ fontWeight: 700, fontSize: '0.95rem', color: '#131921' }}>
                    {u.name}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.4, mt: 0.2 }}>
                    <LocationOn sx={{ fontSize: '0.85rem', color: '#888' }} />
                    <Typography sx={{ fontSize: '0.78rem', color: '#666' }}>
                      {u.city}, {u.state}
                    </Typography>
                  </Box>
                </Box>
              </Button>
            ))}
          </Box>
        </Paper>

        <Divider sx={{ my: 2 }} />
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', textAlign: 'center' }}>
          This is a demo app. No passwords are required.
        </Typography>
      </Box>
    </Box>
  );
};

export default Login;
