import { useState } from 'react';
import { useNavigate } from 'react-router-dom'
import {Box, Button, IconButton, Paper, TextField, FormControl, InputLabel, Input, Typography, InputAdornment} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';

import { login as apiLogin } from '../../services/api';
import { login as authToken} from '../../services/auth';

function LoginPage(){
  const navigate = useNavigate()
  const [nickname, setNickname] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleNicknameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setNickname(event.target.value);
  };

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  }

  const handleLogin = async () => {
    setLoading(true);
    setError('');

    if (nickname === '' || password === '') {
      setError('Preencha todos os campos');
      setLoading(false);
      return;
    }

    const response = await apiLogin(nickname, password).catch((error) => {
      setError(error.response.data.error);
    });

    
    setLoading(false);
    
    if (response?.status === 200) {
      const { token } = response.data;
      authToken(token);
      navigate('/home');

    }

  }

  return (
    <Box sx={{
      width: '100%',
      height: '100vh',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      backgroundImage: 'linear-gradient(45deg, #FE6B8B,#5838ca, #3866ca)',
    }}>
      <Paper sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%',
        maxWidth: '360px',
        height: '100%',
        maxHeight: '500px',
        margin: '0 20px',
      }}>
        <Typography variant="h1" sx={{
          fontSize: '1.8rem',
          fontWeight: 'bold',
          marginTop: '80px',
        }}>
          Car Factory
        </Typography>
        <Box sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}>
          <TextField label="Nickname" variant="standard" value={nickname} onChange={handleNicknameChange} 
            error={error !== ''}
            helperText={error}
          />
          <FormControl variant="standard" sx={{
            marginTop: '8px',
          }}>
            <InputLabel htmlFor="password">Password</InputLabel>
            <Input id='password'  value={password} onChange={handlePasswordChange}
              type={showPassword ? 'text' : 'password'}
              sx={{
                marginTop: '4px',
              }}
              
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={()=>{setShowPassword(!showPassword)}}
                    onMouseDown={(event)=>{event.preventDefault()}}
                    edge="end"
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              }
            />
          </FormControl>  
        </Box>

        <Button variant="contained" 
          onClick={handleLogin}
          sx={{
            margin: '54px 0 40px 0',
            width: '80%',
          }}
        >
          {loading ? 'Loading...' : 'Login'}
        </Button>

      </Paper>
    </Box>
  )
}

export default LoginPage