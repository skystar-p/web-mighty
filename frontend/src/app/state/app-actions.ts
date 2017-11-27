import * as RouterActions from './actions/router';
import * as UserActions from './actions/user';
import * as ProfileActions from './actions/profile';
import * as RoomActions from './actions/room';
import * as WebSocketActions from './actions/websocket';
import { RouterNavigationAction } from '@ngrx/router-store';

export type AppActions
  = RouterActions.Actions
  | UserActions.Actions
  | ProfileActions.Actions
  | RoomActions.Actions
  | WebSocketActions.Actions
  | RouterNavigationAction;
