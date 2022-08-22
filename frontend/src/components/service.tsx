import { MoreVert } from "@mui/icons-material";
import { Box, Button, Chip, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, FormControl, InputLabel, Menu, MenuItem, Select, SelectChangeEvent, TextField, Typography } from "@mui/material";
import { useState } from "react";
import { ServiceElementProps } from "../interfaces/service";
import { convertTimeHoursToExtension } from "../utils/time";
import { statusColor } from "./maintenance";

import {putServiceById, deleteServiceById} from '../services/api'

export function ServiceElement(props: ServiceElementProps){

  const { service } = props

  const [openDialog, setOpenDialog] = useState(false);
  const [openDialogDelete, setOpenDialogDelete] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const [newDescription, setNewDescription] = useState<string>(service?.description || "");
  const [newStatus, setNewStatus] = useState<string>(service?.status || "pending");
  const [newTime, setNewTime] = useState<number>(service?.time);

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

  const handleChangeSelect = (event: SelectChangeEvent) => {
    setNewStatus(event.target.value as string);
  };

  return (
    <>
            <Typography variant="body2" color="text.secondary">Service</Typography>
            <Typography gutterBottom variant="h5" component="div">
                {service?.description}
            </Typography>
            <Box
              sx={{
                position: 'absolute',
                top: '12px',
                right: '16px',
              }}
            >
              <Chip label={service?.status} 
                sx={{
                    
                    backgroundColor: statusColor(service?.status),
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
                Time: {convertTimeHoursToExtension(service?.time)}
            </Typography>
            <Dialog open={openDialog} onClose={handleCloseDialog}>
              <DialogTitle>Edit Service</DialogTitle>
              <DialogContent>
                <DialogContentText>
                  Please, edit service info
                </DialogContentText>
                <TextField
                  autoFocus
                  margin="dense"
                  id="description"
                  label="Describe the service"
                  type="text"
                  fullWidth
                  variant="standard"
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                />
                <TextField
                  label="Time in hours"
                  fullWidth
                  type="number"
                  value={newTime}
                  onChange={(e) => {
                    const t = parseInt(e.target.value);
                      setNewTime(t);
                  }}
                  InputLabelProps={{
                    shrink: true,
                  }}
                  variant="standard"
                />
                <FormControl fullWidth
                  sx={{
                    marginTop: '16px',
                  }}
                >
                  <InputLabel id="select-status-label">Status</InputLabel>
                  <Select
                    labelId="select-status-label"
                    id="select-status"
                    value={newStatus}
                    label="Status"
                    onChange={handleChangeSelect}
                  >
                    <MenuItem value={"done"}>Done</MenuItem>
                    <MenuItem value={"inProgress"}>In Progress</MenuItem>
                    <MenuItem value={"pending"}>Pending</MenuItem>
                  </Select>
                </FormControl>
              </DialogContent>
              <DialogActions>
                <Button onClick={handleCloseDialog}>Cancel</Button>
                <Button onClick={()=>{
                  if(
                    newDescription !== "" && 
                    newStatus !== "" &&
                    newTime >= 0
                  ){
                     putServiceById(service?.id, {
                      description: newDescription,
                      status: newStatus,
                      time: newTime,
                     }).then((res)=>{
                        console.log(res)
                        window.location.reload()
                     }).catch((err)=>{
                        console.log(err)
                     })
                  }
                  handleCloseDialog()
                }}>Update</Button>
              </DialogActions>
            </Dialog>

            <Dialog open={openDialogDelete} onClose={handleCloseDialogDelete}>
              <DialogTitle>Delete Service</DialogTitle>
              <DialogContent>
                <DialogContentText>
                  Are you sure you want to delete this service with descrtipion: <b>{service?.description}</b>?
                </DialogContentText>
              </DialogContent>
              <DialogActions>
                <Button onClick={handleCloseDialogDelete}>Cancel</Button>
                <Button 
                  sx={{color: 'red'}}
                  onClick={()=>{
                    deleteServiceById(service?.id)
                    .then(res=>{
                      window.location.reload()
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