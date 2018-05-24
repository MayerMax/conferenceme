import { Injectable } from '@angular/core';
import {Conference} from "../constructor/models/Conference";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, } from "rxjs/Observable";
import  "rxjs/add/operator/map";
import {ReplaySubject} from "rxjs/ReplaySubject";
import {Subject} from "rxjs/Subject";

@Injectable()
export class StoreService {
   ConferenceSubject$ = new ReplaySubject<Conference>(null);
   Loading = true;
   private BaseUrl = 'http://localhost:8080/conference';
   constructor(private  http: HttpClient)  {
  }
  public getData(id: number){
    let url = `${this.BaseUrl}/${id}`
    console.log(url);
      return this.http.get<Conference>(url).map(
        conference => {
          if (conference != null) {
            console.log(conference);
            conference.begin_date = Conference.parseDate(conference.begin_date);
            conference.end_date = Conference.parseDate(conference.end_date);
            conference.lectures.map((lecture)=>{
              console.log(lecture.date);
              lecture.date = Conference.parseDate(lecture.date);
              return lecture;
            })
          }
          return conference;
        }
      ).subscribe(this.ConferenceSubject$);

    // return this.http.get<Conference>(this.BaseUrl);
  }
  updateConfernce(conference: Conference){
  const BaeUrl = 'http://localhost:8080/conference';
  console.log(conference)
     this.http.post(BaeUrl, conference).subscribe(
          (data) => {
            console.log(data);
            this.ConferenceSubject$.next(conference);
          },
          err => { console.log(err); }
          )

  }
  createConference(){
    this.ConferenceSubject$.next(

      new Conference()
    )
  }
  filterConferenceByIdLecture(idLecture){
    this.ConferenceSubject$.subscribe(
      conference => {
        conference.speakers = conference.speakers.filter((speaker)=> speaker.lection_id == idLecture);
        return conference;
      }
    )
  }

  // public postData(){
  //   return this.http.post(this.BaseUrl,this.Conference).do(
  //     () => {this.Loading =false; })
  // }
  public parseDate(date){
    console.log(date.constructor);
    if (date.constructor  === 'string'){
      return  new Date(date[0],date[1],date[2]);
    }
   return date;
  }
}
