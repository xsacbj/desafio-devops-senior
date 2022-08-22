import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import {Box, Container, Card, Fab, Typography, List, ListItem, CardActionArea, CardContent, Chip, Dialog, DialogTitle, DialogContent, TextField, DialogContentText, DialogActions, Button, FormControl, InputLabel, Select, MenuItem, SelectChangeEvent} from '@mui/material'
import { Add } from '@mui/icons-material'

import { getMaintenances, postMaintenance } from '../../services/api'
import { convertTimeHoursToExtension, formatDateTime } from '../../utils/time'

import { Maintenance } from '../../interfaces/maintenance'
import { statusColor } from '../../components/maintenance'


function HomePage(){

  const navigate = useNavigate()
  const [maintenances, setMaintenances] = useState<Maintenance[]>([])
  const [openDialog, setOpenDialog] = useState(false);
  const [newLicensePlate, setNewLicensePlate] = useState<string>("");
  const [filterStatus, setFilterStatus] = useState<string>("");

  useEffect(() => {
    getMaintenances().then((response) => {
      setMaintenances(response.data.maintenances)
    }).catch((error) => {
      console.log(error)
    })
  }, [])

  const handleClickDialog= () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  function handleChangeStatus(event: SelectChangeEvent) {
    setFilterStatus(event.target.value as string);
  }

  

  function goToMaintenance(id: number){
    navigate(`/maintenance/${id}`)
  }

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
        <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
          <InputLabel id="select-status-label">Status</InputLabel>
          <Select
            labelId="select-status-label"
            id="select-status"
            value={filterStatus}
            label="Status"
            onChange={handleChangeStatus}
          >
            <MenuItem value="">
              <em>All</em>
            </MenuItem>
            <MenuItem value={"done"}>Done</MenuItem>
            <MenuItem value={"inProgress"}>In Progress</MenuItem>
            <MenuItem value={"pending"}>Pending</MenuItem>
          </Select>
        </FormControl>
      </Container>
      <Container>
        <List>
          {maintenances.length>0?
            maintenances
              .filter((maintenance) => {
                if (filterStatus === "") return true;
                return maintenance.status === filterStatus;
              })
              .map((maintenance:any) => (
              <ListItem key={`maintenance_id_${maintenance.id}`}
                sx={{
                display: 'flex',
                justifyContent: 'center',
                }}
              >
                <Card 
                  onClick={() => {
                    goToMaintenance(maintenance.id)
                  }}
                  sx={{ 
                    width: '100%',
                    minWidth: 345,
                    maxWidth: 445,
                    animation: 'none'
                  }}
                >
                  <CardActionArea>
                    <CardContent>
                      <Typography variant="body2" color="text.secondary">License Plate</Typography>
                      <Typography gutterBottom variant="h5" component="div">
                        {maintenance.licensePlate}
                      </Typography>
                      <Chip label={maintenance.status} 
                        sx={{
                          position: 'absolute',
                          top: '12px',
                          right: '16px',
                          backgroundColor: statusColor(maintenance.status),
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
            : (
              <ListItem sx={{
                display: 'flex',
                justifyContent: 'center',
                }}>
                <Typography variant="body1">No maintenances has found</Typography>
              </ListItem>
            )
          }
        </List>

        <Fab aria-label="add" sx={{
            backgroundColor: '#3f51b5',
            position: 'absolute',
            bottom: '20px',
            right: 'calc(15% - 20px)',
          }}
          onClick={handleClickDialog}
        >
          <Add sx={{
            color: '#fff',
          }}/>
        </Fab>
      </Container>
      <Dialog open={openDialog} onClose={handleCloseDialog}>
              <DialogTitle>Create Maintenance</DialogTitle>
              <DialogContent>
                <DialogContentText>
                  Please, enter a new license plate
                </DialogContentText>
                <TextField
                  autoFocus
                  margin="dense"
                  id="licensePlate"
                  label="License Plate"
                  type="text"
                  fullWidth
                  variant="standard"
                  value={newLicensePlate}
                  onChange={(e) => setNewLicensePlate(e.target.value)}
                />
              </DialogContent>
              <DialogActions>
                <Button onClick={handleCloseDialog}>Cancel</Button>
                <Button onClick={()=>{
                  if(newLicensePlate !== ""){
                    postMaintenance({
                      licensePlate: newLicensePlate
                    })
                    .then(res=>{
                      window.location.reload()
                    })
                    .catch((err)=>{
                      console.log(err)
                    })
                  }
                  handleCloseDialog()
                }}>Create</Button>
              </DialogActions>
            </Dialog>
    </Box>
  )
}

export default HomePage