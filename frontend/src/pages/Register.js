import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// Registration is disabled in demo mode — redirect to the user picker.
const Register = () => {
  const navigate = useNavigate();
  useEffect(() => { navigate('/login', { replace: true }); }, [navigate]);
  return null;
};

export default Register;
