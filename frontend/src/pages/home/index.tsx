import {Box, Container, Card, Button,Fab, Typography, List, ListItem, CardActionArea, CardContent, Chip} from '@mui/material'
import { useState } from 'react'
import { Add } from '@mui/icons-material'

import { convertTimeHoursToExtension, formatDateTime } from '../../utils/time'

function Home(){

  const [maintenances, setMaintenances] = useState<any>([
    {
      id: 1,
      licensePlate: "JTN-9005",
      timeEstimate: 240,
      status: "done",
      createAt: "2022-08-19T03:00:30"
    },
    {
      id: 2,
      licensePlate: "JTN-9005",
      timeEstimate: 240,
      status: "done",
      createAt: "2022-08-19T03:00:30"
    }
  ])



  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <Container
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          margin: '20px 24px 40px 24px' ,
        }}
      >
        <Typography variant="h1"
          sx={{
            fontSize: '2.2rem',
            width: 'fit-content',
          }}
        >
          Maintenances
        </Typography>
        
      </Container>
      <Container>
        <List>
          {maintenances?
            maintenances.map((maintenance:any) => (
              <ListItem key={`maintenance_id_${maintenance.id}`}
                sx={{
                display: 'flex',
                justifyContent: 'center',
                }}
              >
                <Card sx={{ 
                  width: '100%',
                  minWidth: 345,
                  maxWidth: 445,
                }}>
                  <CardActionArea>
                    <CardContent>
                      <Typography gutterBottom variant="h5" component="div">
                        {maintenance.licensePlate}
                      </Typography>
                      <Chip label={maintenance.status} 
                        sx={{
                          backgroundColor: '#4caf50',
                          color: '#fff',
                          margin: '0 0 20px  0',
                        }}
                      />
                      <Typography variant="body2" color="text.secondary">
                        Estimated time: {convertTimeHoursToExtension(maintenance.timeEstimate)}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Created at: {formatDateTime(maintenance.createAt)}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </ListItem>
            ))
            : null
          }
        </List>
      </Container>
      <Fab aria-label="add" sx={{
          backgroundColor: '#3f51b5',
          position: 'fixed',
          bottom: '20px',
          right: '10%',
          minRight: '80px',
        }}>
          <Add sx={{
            color: '#fff',
          }}/>
        </Fab>
    </Box>
  )
}

export default Home