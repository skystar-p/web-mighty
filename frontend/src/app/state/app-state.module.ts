import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { CommonModule } from '@angular/common';

import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { StoreRouterConnectingModule } from '@ngrx/router-store';

import { WebSocketService } from './websocket.service';

// Reducers
import { reducers } from './reducer';

// Effects
import { UserEffects } from './effects/user';
import { RouterEffects } from './effects/router';
import { ProfileEffects } from './effects/profile';
import { RoomEffects } from './effects/room';
import { WebSocketEffects } from './effects/websocket';
import { GameEffects } from './effects/game';
import { HallOfFameEffects } from './effects/hall-of-fame';

@NgModule({
  imports: [
    CommonModule,
    HttpModule,
    StoreModule.forRoot(reducers),
    EffectsModule.forRoot([
      UserEffects,
      ProfileEffects,
      RouterEffects,
      RoomEffects,
      WebSocketEffects,
      GameEffects,
      HallOfFameEffects,
    ]),
    StoreRouterConnectingModule,
  ],
  declarations: [],
  providers: [
    WebSocketService,
  ],
  exports: [
    StoreModule,
    EffectsModule,
  ],
})
export class AppStateModule { }
