import React from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions,
  Button, Typography
} from '@mui/material';

interface ConfirmDialogProps {
  open: boolean;
  message: string;
  onClose: () => void;
  onConfirm: () => void;
}

const ConfirmDialog: React.FC<ConfirmDialogProps> = ({ open, message, onClose, onConfirm }) => (
  <Dialog
    open={open}
    onClose={onClose}
    PaperProps={{
      sx: {
        backgroundColor: '#fff',
        color: '#000',
      }
    }}
  >
    <DialogTitle>Confirm Deletion</DialogTitle>
    <DialogContent>
      <Typography>{message}</Typography>
    </DialogContent>
    <DialogActions>
      <Button onClick={onClose}>Cancel</Button>
      <Button color="error" variant="contained" onClick={onConfirm}>Delete</Button>
    </DialogActions>
  </Dialog>
);

export default ConfirmDialog;
