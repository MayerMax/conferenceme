// import {Component, Inject, Injectable} from '@angular/core';
// import {Observable} from "rxjs/Observable";
// import {ActivatedRouteSnapshot, CanDeactivate, Router, RouterStateSnapshot} from "@angular/router";
// import {MAT_DIALOG_DATA, MatDialog, MatDialogConfig, MatDialogRef} from "@angular/material";
// import {Speaker} from "../constructor/models/speaker";
// import {Lecture} from "../constructor/models/lecture";
// export interface CanComponentDeactivate {
//   canDeactivate: () => Observable<boolean> | Promise<boolean> | boolean;
// }
// @Injectable()
// export class CanDeactiveGuardService implements CanDeactivate<CanComponentDeactivate> {
//
//   constructor(public dialog: MatDialog, private router: Router) {
//   }
//   openDialog(companent, nextState ): Observable<boolean> {
//     let answer;
//     let dialogRef = this.dialog.open(DialogOverviewExampleDialog,  {
//       width: '400px',
//       height: '350px',
//       data: companent.model
//     } as MatDialogConfig<any>);
//     return dialogRef.afterClosed();
// }
//   canDeactivate(component,
//                 route: ActivatedRouteSnapshot,
//                 state: RouterStateSnapshot,
//                 nextState: RouterStateSnapshot) {
//
//     console.log(route);
//     console.log(nextState);
//     let url: string = state.url;
//     console.log('Url: ' + url);
//     if (component.canDeactivate()) {
//       return true;
//     } else {
//       this.openDialog(component, nextState).subscribe(
//         data => {
//           if (data === true) {
//             this.router.navigateByUrl(nextState.url);
//             component.sendData = true;
//             console.log(component.model);
//           } else if (data === false) {
//             this.router.navigateByUrl(nextState.url);
//             component.sendData = true;
//           }
//         });
//     }
//     // return component.canDeactivate ? component.canDeactivate() : true;
//   }
// }
// @Component({
//   selector: 'app-dialog-overview-example-dialog',
//   template: `<h1 mat-dialog-title>Сохранить данные и перейти</h1>
//   <div mat-dialog-content>
//     <p>Прикрепить к </p>
//
//     <mat-form-field *ngIf="isSpeaker" >
//       <mat-select  placeholder="Выбрать Лекцию к которой" >
//         <mat-option *ngFor="let nameLecture of data.nameLectures" [value]="nameLecture">{{nameLecture}}</mat-option>
//       </mat-select>
//     </mat-form-field>
//     <mat-form-field   *ngIf="isLecture" >
//       <mat-select placeholder="Выбрать Секцию к которой" >
//         <mat-option *ngFor="let nameLecture of data.nameLectures" [value]="nameLecture">{{nameLecture}}</mat-option>
//       </mat-select>
//     </mat-form-field>
//   </div>
//   <div mat-dialog-actions>
//     <button mat-button (click)="onNoClick()">Назад</button>
//     <button mat-button [mat-dialog-close]="true" cdkFocusInitial>Send</button>
//     <button mat-button [mat-dialog-close]="false" cdkFocusInitial>Не сохранять</button>
//   </div>
//   `})
// export class DialogOverviewExampleDialog {
//   isSpeaker: boolean = false;
//   isLecture: boolean = false;
//   constructor(
//     public dialogRef: MatDialogRef<DialogOverviewExampleDialog>,
//     @Inject(MAT_DIALOG_DATA) public data: any) {
//     console.log(data);
//     if (data instanceof Speaker) {
//       this.isSpeaker = true;
//     }
//     if (data instanceof Lecture) {
//       this.isLecture = true;
//     }
//   }
//
//   onNoClick(): void {
//     this.dialogRef.close();
//   }
// }
