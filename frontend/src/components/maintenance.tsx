import { useState } from 'react';
import { Typography, Chip, Button, Menu, MenuItem, Dialog, DialogTitle, DialogContent, DialogContentText, TextField, DialogActions } from "@mui/material"

import {  MaintenanceElementProps } from '../interfaces/maintenance';
import { convertTimeHoursToExtension, formatDateTime } from '../utils/time';
import { Box } from '@mui/system';
import { MoreVert } from '@mui/icons-material';

import {putMaintenanceById, deleteMaintenanceById} from '../services/api'
import { useNavigate } from 'react-router-dom';

export function statusColor(status?: string){
    switch(status){
      case "done":
        return "#4caf50"
      case "inProgress":
        return "#2196f3"
      case "pending":
        return "#ff9800"
      default:
        return "#000000"
    }
  }

export function MaintenanceElement(props: MaintenanceElementProps):JSX.Element {
    const { maintenance } = props
    const navigate = useNavigate()

    const [openDialog, setOpenDialog] = useState(false);
    const [openDialogDelete, setOpenDialogDelete] = useState(false);
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const [newLicensePlate, setNewLicensePlate] = useState<string>("");
    const open = Boolean(anchorEl);



    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
      setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
      setAnchorEl(null);
    };

    const handleClickDialog= () => {
      setOpenDialog(true);
    };
  
    const handleCloseDialog = () => {
      setOpenDialog(false);
    };

    const handleClickDialogDelete= () => {
      setOpenDialogDelete(true);
    };
  
    const handleCloseDialogDelete = () => {
      setOpenDialogDelete(false);
    };
  

    return (
        <>
            <Typography variant="body2" color="text.secondary">License Plate</Typography>
            <Typography gutterBottom variant="h5" component="div">
                {maintenance?.licensePlate}
            </Typography>
            <Box
              sx={{
                position: 'absolute',
                top: '12px',
                right: '16px',
              }}
            >
              <Chip label={maintenance?.status} 
                sx={{
                    
                    backgroundColor: statusColor(maintenance?.status),
                    color: '#fff',
                }}  
              />
              <Button
                id="basic-button"
                aria-controls={open ? 'basic-menu' : undefined}
                aria-haspopup="true"
                aria-expanded={open ? 'true' : undefined}
                onClick={handleClick}
                sx={{
                  minWidth: '0px',
                  paddingRight: '0px',
                }}
              >
                <MoreVert />
              </Button>
              <Menu
                id="basic-menu"
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                MenuListProps={{
                  'aria-labelledby': 'basic-button',
                }}
              >
                <MenuItem onClick={()=>{
                  handleClickDialog()
                  handleClose()
                }}>Edit</MenuItem>
                <MenuItem sx={{color: 'red'}} onClick={()=>{
                  handleClickDialogDelete()
                  handleClose()
                }}>Delete</MenuItem>
              </Menu>
            </Box>
            <Typography variant="body2" color="text.secondary">
                Estimated time: {convertTimeHoursToExtension(maintenance?.timeEstimate)}
            </Typography>
            <Typography variant="body2" color="text.secondary">
                Created at: {formatDateTime(maintenance?.createAt)}
            </Typography>
            <Dialog open={openDialog} onClose={handleCloseDialog}>
              <DialogTitle>Edit License Plate</DialogTitle>
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
                  if(newLicensePlate !== "" && newLicensePlate !== maintenance?.licensePlate){
                    putMaintenanceById(maintenance?.id, {
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
                }}>Update</Button>
              </DialogActions>
            </Dialog>

            <Dialog open={openDialogDelete} onClose={handleCloseDialogDelete}>
              <DialogTitle>Delete Maintenance</DialogTitle>
              <DialogContent>
                <DialogContentText>
                  Are you sure you want to delete this maintenance
                  with license plate <b>{maintenance?.licensePlate}</b>?
                </DialogContentText>
              </DialogContent>
              <DialogActions>
                <Button onClick={handleCloseDialogDelete}>Cancel</Button>
                <Button 
                  sx={{color: 'red'}}
                  onClick={()=>{
                    deleteMaintenanceById(maintenance?.id)
                    .then(res=>{
                      navigate('/home')
                    })
                    .catch((err)=>{
                      console.log(err)
                    })
                    handleCloseDialogDelete()
                  }}
                >Delete</Button>
              </DialogActions>
            </Dialog>
        </>
    );
}